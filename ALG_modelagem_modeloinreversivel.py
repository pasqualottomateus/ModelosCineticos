from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# =================================================================
#                   DADOS EXPERIMENTAIS (% CONVERSÃO)
# =================================================================
t_comum = np.array([0, 5, 10, 20, 30, 60, 120, 180, 240])  # Tempos (min)
C_media = np.array([0, 48.1, 50.9, 58.9, 62.2, 76.2, 86.1, 88.3, 88.9])  # %

# =================================================================
#               PARÂMETROS DO SISTEMA
# =================================================================
C_A0 = 0.177  # Concentração inicial do ácido oleico (mol/L)
C_B0 = 3.54   # Concentração do metanol (mol/L)

# =================================================================
#               MODELO IREVERSÍVEL COM ÁGUA 
# =================================================================
def modelo_reversivel(t, k_f, K_A, K_B, K_D):

    def dXdt(t, X):
        C_A = C_A0 * (1 - X/100)
        C_B = C_B0 - C_A0 * X/100
        C_D = C_A0 * X/100  # Água produzida
        
        # Termos do numerador e denominador
        numerador = k_f * K_A * K_B * C_A * C_B
        denominador = (1 + K_A*C_A + K_B*C_B + K_D*C_D)**2
        
        taxa = numerador / denominador
        return taxa * 100 / C_A0  # %/min
    
    sol = solve_ivp(
        dXdt,
        [0, np.max(t)],
        [0],
        t_eval=t,
        method='BDF',
        rtol=1e-6,
        atol=1e-9
    )
    return sol.y[0]

# =================================================================
#               AJUSTE DE PARÂMETROS 
# =================================================================
params_iniciais = [0.1, 0.1, 0.1, 0.1]  # k_f, K_A, K_B, k_r, K_D
bounds = ([1e-5, 1e-3, 1e-3, 1e-3], [1e3, 1e3, 1e3, 1e3])  # Limites

try:
    popt, pcov = curve_fit(
        modelo_reversivel,
        t_comum,
        C_media,
        p0=params_iniciais,
        bounds=bounds,
        maxfev=100000  # iterações
    )
    k_f, K_A, K_B, K_D = popt
    print("Ajuste bem-sucedido!")
    print(f"k_f = {k_f:.3e}, K_A = {K_A:.3f}, K_B = {K_B:.3f}")
    print(f"K_D = {K_D:.3f}")
    
except Exception as e:
    print(f"Erro no ajuste: {str(e)}")
    popt = params_iniciais  # Usar valores iniciais para plotagem

# =================================================================
#               VISUALIZAÇÃO
# =================================================================
t_ajuste = np.linspace(0, 240, 100)
C_pred = modelo_reversivel(t_ajuste, *popt)

plt.figure(figsize=(12, 6))
plt.scatter(t_comum, C_media, color='black', label='Dados Experimentais', zorder=5)
plt.plot(t_ajuste, C_pred, 'r--', label='Modelo Reversível', linewidth=2)
plt.xlabel('Tempo (min)', fontsize=12)
plt.ylabel('Conversão (%)', fontsize=12)
plt.title('Modelagem Cinética com Efeito da Água', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.ylim(0, 100)
plt.show()

# =================================================================
#               MÉTRICAS DE QUALIDADE
# =================================================================
if 'popt' in locals():
    C_pred = modelo_reversivel(t_comum, *popt)
    print(f"\nR² = {r2_score(C_media, C_pred):.3f}")
    print(f"RMSE = {np.sqrt(mean_squared_error(C_media, C_pred)):.2f}%")
    