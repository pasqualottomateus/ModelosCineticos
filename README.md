Project Overview
Python implementation of a kinetic model for a reversible chemical reaction considering water inhibition effects. The algorithm performs parameter estimation from experimental conversion data and provides model validation metrics.
  Chemical Context
Models the kinetic behavior of a reversible reaction system where water acts as an inhibitor, using a Langmuir-Hinshelwood type mechanism with competitive adsorption.
Model Features
Reversible kinetic model with product inhibition (water)

Competitive adsorption of reactants and products

Non-linear parameter estimation using curve fitting

Numerical integration with adaptive step-size control

Comprehensive model validation with statistical metrics

Model Parameters
The algorithm estimates four kinetic parameters:

Parameter	Description	Units
k_f	Forward reaction rate constant	L·mol⁻¹·min⁻¹
K_A	Adsorption constant for acid	L·mol⁻¹
K_B	Adsorption constant for methanol	L·mol⁻¹
K_D	Adsorption constant for water	L·mol⁻¹

Prerequisites
pip install numpy scipy matplotlib scikit-learn

Parameter Estimation
Method: Non-linear least squares (Levenberg-Marquardt)
Bounds: 10⁻⁵ to 10³ for all parameters
Max iterations: 100,000
Integration: BDF method for stiff equations
Outputs
Optimized kinetic parameters
Model vs experimental plot
Quality metrics: R² and RMSE

Applications
Chemical reaction optimization
Reactor design and scale-up
Catalytic reaction studies
Product inhibition analysis
Process simulation

Parameter Analysis
High K values indicate strong adsorption
K_B/K_A ratio shows adsorption selectivity
k_f determines overall reaction rate

Contributing
Feel free to fork this project and submit pull requests for:
Additional kinetic models
Improved optimization algorithms
Enhanced visualization features
Extended validation methods
