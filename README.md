# SoilSense AI

**Real-Time Intelligence for Soil Nutrient Evaluation and Ecosystem Remediation**

SoilSense AI is a dataset-driven Streamlit educational prototype. Users enter N, P, K, pH, temperature, humidity, and rainfall values. A Random Forest classifier predicts a crop label, while a rule-based module displays general soil findings, remediation suggestions, and environmental considerations.

## Run locally

```bash
python -m pip install -r requirements.txt
python train_model.py
python -m streamlit run app.py
```

On first app launch, the application also attempts to generate the model automatically if `crop_model.pkl` is absent. This requires access to the public dataset URL configured in `train_model.py`.

## Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app** and select repository `atharvshingade-code/soilsense-ai`.
3. Set branch to `main` and main file path to `app.py`.
4. Deploy. The first start may take a few minutes while dependencies install and the model is trained.

## Limitations

- This is an educational prototype, not a validated agricultural diagnostic system.
- Crop prediction depends on the training dataset and does not guarantee crop success.
- NPK measurements are displayed as entered; the application does not independently verify units or nutrient deficiency.
- Remediation suggestions are general. The app does not calculate fertilizer dosages or detect soil contamination.
- The current version uses manual inputs and does not use live sensors.

## Dataset

The training script downloads a Crop Recommendation CSV from the public source configured in `train_model.py`. Confirm the dataset's provenance and license before redistributing the data or using this project commercially.
