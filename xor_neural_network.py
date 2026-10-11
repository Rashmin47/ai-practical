import numpy as np

# XOR truth table: output is 1 when exactly one input is 1.
X = np.array([[0., 0.],
              [0., 1.],
              [1., 0.],
              [1., 1.]])
y = np.array([[0.], [1.], [1.], [0.]])

np.random.seed(3)
# Architecture: 2 input neurons -> 2 tanh hidden neurons -> 1 sigmoid output.
W1 = np.random.randn(2, 2)
b1 = np.zeros((1, 2))
W2 = np.random.randn(2, 1)
b2 = np.zeros((1, 1))
learning_rate = 1.0
epochs = 30000

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

for epoch in range(1, epochs + 1):
    # Forward propagation
    hidden = np.tanh(X @ W1 + b1)
    output = sigmoid(hidden @ W2 + b2)

    # Backpropagation using mean-squared-error derivatives
    error = output - y
    d_output = error                         # sigmoid derivative included by MSE form below
    d_z2 = error * output * (1 - output)
    d_hidden = (d_z2 @ W2.T) * (1 - hidden ** 2)

    W2 -= learning_rate * (hidden.T @ d_z2) / len(X)
    b2 -= learning_rate * np.mean(d_z2, axis=0, keepdims=True)
    W1 -= learning_rate * (X.T @ d_hidden) / len(X)
    b1 -= learning_rate * np.mean(d_hidden, axis=0, keepdims=True)

    if epoch in [1, 1000, 5000, 10000, 20000, 30000]:
        loss = np.mean((output - y) ** 2)
        print(f'Epoch {epoch:5d} | MSE loss = {loss:.10f}')
        print('Outputs:', np.round(output.ravel(), 6))

predicted = (output >= 0.5).astype(int)
print('\nFinal XOR predictions:')
for inputs, value, target in zip(X.astype(int), output.ravel(), y.astype(int).ravel()):
    print(f'{inputs.tolist()} -> probability {value:.6f}, class {int(value >= 0.5)}, target {target}')
print('\nTraining accuracy:', f'{np.mean(predicted == y) * 100:.1f}%')
