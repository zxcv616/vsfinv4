import shap

class ModelInterpretation:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.explainer = shap.Explainer(model)

    def plot_shap_values(self):
        shap_values = self.explainer(self.data)
        shap.summary_plot(shap_values, self.data)
