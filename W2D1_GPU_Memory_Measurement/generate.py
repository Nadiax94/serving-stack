
import torch, time
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

def load(dtype):
    tok = AutoTokenizer.from_pretrained(MODEL_ID)

    if dtype == "fp16":
        m = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            device_map="cuda"
        )

    elif dtype == "int8":
        m = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            quantization_config=BitsAndBytesConfig(load_in_8bit=True),
            device_map="cuda"
        )

    elif dtype == "int4":
        m = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            quantization_config=BitsAndBytesConfig(load_in_4bit=True),
            device_map="cuda"
        )

    return tok, m


def tokens_per_s(dtype, new_tokens=128):

    tok, m = load(dtype)

    ids = tok(
        "Explain what a GPU does.",
        return_tensors="pt"
    ).input_ids.to("cuda")

    m.generate(
        input_ids=ids,
        max_new_tokens=8
    )

    torch.cuda.synchronize()

    start = time.time()

    out = m.generate(
        input_ids=ids,
        max_new_tokens=new_tokens,
        do_sample=False
    )

    torch.cuda.synchronize()

    end = time.time()

    generated = out.shape[1] - ids.shape[1]

    return generated/(end-start)
