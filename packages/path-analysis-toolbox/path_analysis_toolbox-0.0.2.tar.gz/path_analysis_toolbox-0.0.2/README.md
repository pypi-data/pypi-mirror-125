Get directory, filename or extension from path:
```python
from path_analysis_toolbox import PathAnalyser
PathAnalyser.directory_filename_extension("C:\\Example\\directory\\filename.mp3")
# ("C:\\Example\\directory", "filename", "mp3")

PathAnalyser.directory("C:\\Example\\directory\\filename.mp3") # "C:\\Example\\directory"
PathAnalyser.filename("C:\\Example\\directory\\filename.mp3") # "filename"
PathAnalyser.extension("C:\\Example\\directory\\filename.mp3") # "mp3"

PathAnalyser.directory_filename_extension("C:\\Example\\directory\\filename")
# ("C:\\Example\\directory", "filename", "")
PathAnalyser.directory_filename_extension("C:")
# ("", "C:", "")
```