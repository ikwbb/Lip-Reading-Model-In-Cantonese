import torch
import argparse

def ensemble(checkpoint_path, save_path):
    states = torch.load(checkpoint_path, map_location=lambda storage, loc: storage)["state_dict"]
    states = {k[6:]: v for k, v in states.items() if k.startswith("model.")}
    torch.save(states, save_path)
    return save_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert checkpoint to PyTorch model")
    parser.add_argument('--checkpoint', type=str, required=True, help='Input checkpoint file path')
    parser.add_argument('--output', type=str, required=True, help='Output PyTorch model file path')
    args = parser.parse_args()

    if hasattr(args, 'help'):
        print("Example usage: python script.py --checkpoint /path/to/epoch_20.ckpt --output /path/to/model_20.pth")
    else:
        ensemble(args.checkpoint, args.output)