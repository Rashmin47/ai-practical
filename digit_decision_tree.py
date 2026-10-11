from pathlib import Path
import numpy as np
from PIL import Image
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

DATA_DIR = Path('handwritten_digit_corpus')
PLOT_PATH = Path('digit_10fold_results.png')
SAMPLE_PATH = Path('digit_samples.png')

files = sorted(DATA_DIR.glob('*.png'))
X = np.asarray([np.asarray(Image.open(p).convert('L'), dtype=np.float32).ravel() / 255.0 for p in files])
y = np.asarray([int(p.stem.split('_')[0]) for p in files])

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
model = DecisionTreeClassifier(random_state=42, criterion='gini')
scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy', n_jobs=-1)

print('Dataset samples:', len(files))
print('Feature shape:', X.shape)
print('Classes:', sorted(np.unique(y).tolist()))
print('Fold accuracies:', [round(float(s), 6) for s in scores])
print('Mean accuracy:', round(float(scores.mean()), 6))
print('Std. deviation:', round(float(scores.std()), 6))
print('Min accuracy:', round(float(scores.min()), 6))
print('Max accuracy:', round(float(scores.max()), 6))

plt.figure(figsize=(8, 4.8))
folds = np.arange(1, 11)
plt.plot(folds, scores * 100, marker='o', linewidth=2.2, color='#1f4e78', label='Fold accuracy')
plt.axhline(scores.mean() * 100, color='#e67e22', linestyle='--', linewidth=1.8, label=f'Mean = {scores.mean()*100:.2f}%')
plt.xticks(folds)
plt.ylim(max(0, scores.min()*100 - 5), min(100, scores.max()*100 + 5))
plt.xlabel('Cross-validation fold')
plt.ylabel('Accuracy (%)')
plt.title('Decision Tree: Stratified 10-Fold Cross-Validation')
plt.grid(axis='y', alpha=.25)
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_PATH, dpi=180)
plt.close()

rng = np.random.default_rng(42)
indices = rng.choice(len(files), 16, replace=False)
fig, axes = plt.subplots(4, 4, figsize=(5, 5))
for ax, idx in zip(axes.ravel(), indices):
    ax.imshow(X[idx].reshape(28, 28), cmap='gray')
    ax.set_title(f'Label: {y[idx]}', fontsize=9)
    ax.axis('off')
fig.suptitle('Sample Images from Downloaded Handwritten-Digit Dataset', fontsize=12)
fig.tight_layout()
fig.savefig(SAMPLE_PATH, dpi=180, bbox_inches='tight')
plt.close(fig)
