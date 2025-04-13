import torch

# 定义常量变量，直接使用字符串路径
CHECKPOINT_PATH = "/home/mint/FYP/auto_avsr/exp_finetune/cantonese_vsr_best/epoch=20.ckpt"
SAVE_PATH = "/home/mint/FYP/auto_avsr/exp_finetune/cantonese_vsr_best/model_20.pth"

def ensemble():
    # 使用常量变量指定检查点路径
    last_checkpoint = CHECKPOINT_PATH
    # 加载检查点的状态字典
    states = torch.load(last_checkpoint, map_location=lambda storage, loc: storage)["state_dict"]
    # 移除键中的 "model." 前缀，与原逻辑一致
    states = {k[6:]: v for k, v in states.items() if k.startswith("model.")}
    # 使用常量变量指定保存路径
    model_path = SAVE_PATH
    # 保存处理后的状态字典
    torch.save(states, model_path)
    return model_path

if __name__ == "__main__":
    ensemble()