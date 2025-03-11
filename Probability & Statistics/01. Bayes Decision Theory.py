import numpy as np
import matplotlib.pyplot as plt

# 설정값
classes = ['Class A', 'Class B']
prior = np.array([0.6, 0.4])  # 사전 확률

# Likelihood 정의 (조건부 확률)
def likelihood(x, cls):
    if cls == 'Class A':
        return np.exp(-(x - 2)**2 / (2 * 1**2)) / (np.sqrt(2 * np.pi) * 1)
    elif cls == 'Class B':
        return np.exp(-(x - 5)**2 / (2 * 1.5**2)) / (np.sqrt(2 * np.pi) * 1.5)

# Posterior Probability 계산
def posterior(x):
    likelihoods = np.array([likelihood(x, cls) for cls in classes])
    numerator = likelihoods * prior
    return numerator / np.sum(numerator)

# x축 설정
x = np.linspace(-2, 10, 500)

# Likelihood 시각화
plt.figure(figsize=(10, 5))
for cls in classes:
    plt.plot(x, [likelihood(xi, cls) for xi in x], label=f'Likelihood {cls}')
plt.title('Likelihood (Conditional Probabilities)')
plt.xlabel('x')
plt.ylabel('p(x|Class)')
plt.legend()
plt.grid()
plt.show()

# Posterior Probability 시각화
posterior_probs = np.array([posterior(xi) for xi in x])
plt.figure(figsize=(10, 5))
plt.plot(x, posterior_probs[:, 0], label='Posterior Class A')
plt.plot(x, posterior_probs[:, 1], label='Posterior Class B')
plt.title('Posterior Probabilities')
plt.xlabel('x')
plt.ylabel('Posterior Probability p(Class|x)')
plt.legend()
plt.grid()
plt.show()