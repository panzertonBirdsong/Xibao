from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
    low_cpu_mem_usage=True
)

# Save to disk
model.save_pretrained("./deepseek-model")
tokenizer.save_pretrained("./deepseek-model")