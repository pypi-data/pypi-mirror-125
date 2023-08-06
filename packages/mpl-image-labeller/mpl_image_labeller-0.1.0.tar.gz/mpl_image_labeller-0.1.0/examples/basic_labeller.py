import matplotlib.pyplot as plt
import numpy as np

from mpl_image_labeller import image_labeller

images = np.random.randn(5, 10, 10)
labeller = image_labeller(
    images, classes=["good", "bad", "mejslkdj;flksjdh"], label_keymap=["a", "s", "d"]
)
plt.show()
print(labeller.labels)
