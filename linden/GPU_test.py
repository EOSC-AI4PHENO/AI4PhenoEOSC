import tensorflow as tf
import sys

print("Python version")
print(sys.version)
#print("Version info.")
#print(sys.version_info)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

#if tf.test.is_gpu_available():
#    print("GPU is available")
#    print("GPU devices:", tf.config.list_physical_devices('GPU'))
#else:
#    print("GPU is not available")