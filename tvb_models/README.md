## Generating `.pth` Files

To convert trained VSR model checkpoints to `.pth` format, follow these steps:

1. **Navigate to the Script Directory**  
   Ensure you are in the correct directory containing the conversion script:

   ```
   Step_3_Visual_Speech_Recognition_Model_Training/Step_4_VSR_Model_Training/trained_vsr_models/
   ```

2. **Run the Conversion Script**  
   Execute the `ckpt_to_pth.py` script to generate `.pth` files from the trained checkpoints:

   ```bash
   python ckpt_to_pth.py
   ```

3. **Output Naming Convention**  
   The script will save the converted files with the naming format `epoch=<number>.pth`, e.g., `epoch=59.pth`. Ensure the script is configured to match this convention