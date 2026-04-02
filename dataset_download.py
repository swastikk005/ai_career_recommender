import kagglehub

# Download latest version
path = kagglehub.dataset_download("avishekmajhi/resume-dataset")

print("Path to dataset files:", path)