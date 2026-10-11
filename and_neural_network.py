import numpy as np

# AND truth table: output is 1 only when both inputs are 1.
X = np.array([[0., 0.],
              [0., 1.],
              [1., 0.],
              [1., 1.]])
y = np.array([[0.], [0.], [0.], [1.]])

np.random.seed(12)
# Appropriate architecture for linearly separable AND: 2 inputs -> 1 sigmoid output.
weights = np.random.randn(2, 1)
bias = np.zeros((1, 1))
learning_rate = 1.0
epochs = 5000

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

for epoch in range(1, epochs + 1):
    # Forward propagation
    output = sigmoid(X @ weights + bias)

    # Backpropagation using binary cross-entropy gradient
    error = output - y
    weights -= learning_rate * (X.T @ error) / len(X)
    bias -= learning_rate * np.mean(error, axis=0, keepdims=True)

    if epoch in [1, 100, 1000, 2500, 5000]:
        loss = -np.mean(y * np.log(output + 1e-9) +
                        (1 - y) * np.log(1 - output + 1e-9))
        print(f'Epoch {epoch:4d} | BCE loss = {loss:.10f}')
        print('Outputs:', np.round(output.ravel(), 6))

predicted = (output >= 0.5).astype(int)
print('\nFinal AND predictions:')
for inputs, value, target in zip(X.astype(int), output.ravel(), y.astype(int).ravel()):
    print(f'{inputs.tolist()} -> probability {value:.6f}, class {int(value >= 0.5)}, target {target}')
print('\nTraining accuracy:', f'{np.mean(predicted == y) * 100:.1f}%')
print('Learned weights:', np.round(weights.ravel(), 6))
print('Learned bias:', np.round(bias.ravel(), 6))
