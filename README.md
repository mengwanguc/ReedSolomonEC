
## Heatmap Generation Steps:

- Command to run the heatmap generation script: ```python heatmap.py [-n -k -m -o]```
- Arguments:
  - n = Number of data shards (default = 17).
  - k = Number of parity shards (defualt = 3).
  - c = Chunksize in KB (default = 128).
  - m = Mode (default = i):
    - i to use the ISA-L tool.
    - j to use the JavaReedSolomon tool.
  - o = Heatmap filename with appropriate image extension (default = heatmap.png).

## Notes About Submodules:

- The ```isa-l``` submodule needs to be on the ```ReedSolomon``` branch.
- The ```JavaReedSolomon``` submodule is based on the [Backblaze Java Reed-Solomon repository](https://github.com/Backblaze/JavaReedSolomon).
- The ```isa-l``` submodule is forked from the [Intel ISA-L repository](https://github.com/intel/isa-l).
