# Uncertainty and Active Vision

Research code for investigating **uncertainty-aware visual recognition and active visual perception under occlusion**.

The project asks whether obtaining an additional observation from a different camera viewpoint can help a vision system recognize objects that are difficult to identify from an initial image. It explores this question with the BOP YCB-Video (YCB-V) dataset and complementary synthetic-image experiments.

The work is an offline perception study. It uses viewpoint variation in image data to examine the potential benefit of an alternative observation; it does not implement a complete mobile robot, autonomous navigation policy, reinforcement learning system, or physical camera movement.

## Research motivation

A single image may contain incomplete evidence about an object because of occlusion, viewpoint, or visual ambiguity. An embodied system may be able to improve its perception by observing the same scene from another angle.

However, another observation is not necessarily useful. It may reveal new object information, repeat the same ambiguity, or even make recognition more difficult. This project studies when additional visual evidence can help and how recognition outcomes relate to uncertainty.

## Repository contents

### Notebooks

| Notebook | Purpose |
|---|---|
| `YCB-V_Dataset_Analysis (1).ipynb` | Explore the YCB-V dataset, its scenes, object categories, annotations, visibility, and candidate data for experiments. |
| `Experiment_Real_Images (1).ipynb` | Run and analyse experiments using real YCB-V images and object observations. |
| `Experiment_Synthetic_images (1).ipynb` | Run and analyse complementary experiments with synthetic images. |

The notebooks contain the main analysis and experimental workflow. Notebook outputs may reflect the data and paths available in the original development environment.

### Python preprocessing and dataset utilities

The repository also includes scripts for obtaining, inspecting, selecting, extracting, and preparing YCB-V data.

| Script | Purpose |
|---|---|
| `download_ycbv.py` | Download the YCB-V dataset files from the Hugging Face dataset repository. |
| `check_7zipfile.py` | Check whether 7-Zip is installed and available. |
| `check_ycbv_volumes.py` | Check for the expected parts of a split multi-volume YCB-V archive. |
| `inspect_ycbv.py` | Inspect selected scenes from the synthetic `train_pbr` split and summarize object-category coverage. |
| `extract_ycbv_subset.py` | Extract a smaller synthetic training/validation subset, including selected RGB images and annotations. |
| `inspect_ycbv_real.py` | Inspect the real-image YCB-V archive. |
| `extract_real_annotations.py` | Extract scene annotation files from the real-image archive. |
| `prepare_real_subsets.py` | Select real-image frames across chosen scenes and write an image-path list. |
| `extract_real_images.py` | Extract selected real RGB images from the archive. |
| `prepare_real_annotations.py` | Filter scene annotations to the selected images and save train/validation split information. |
| `analyse_real_annotations.py` | Summarize real-image scene, object-instance, and visibility coverage. |
| `inspect_distribution.py` | Inspect the distribution of selected object categories across real-image scenes. |
| `inspect_scene_categories.py` | Examine category coverage and visible instances by scene. |
| `extract_selected_rgb.py` | Extract a specified list of RGB images from the real-image archive. |
| `test_extract_real.py` | Test extraction of an individual real-image sample. |
| `zip_real_subset.py` | Package the prepared real-image subset for transfer or use in a notebook environment. |

Some scripts are utilities used during dataset exploration and preparation rather than required steps in every experiment.

## Dataset

The experiments use the **BOP YCB-Video (YCB-V)** dataset. It provides RGB images of common objects in scenes, along with camera and object annotations. The annotations support analysis of object identity, camera viewpoint, and visible object fraction.

The repository does not include the full original dataset. The dataset is large, so it should be downloaded separately and only the required subset should be prepared.

The preprocessing scripts work with the YCB-V archive structure and include Windows paths from the original development environment. Update those paths to match your own machine or mounted Google Drive before running them.

## Experimental approach

The project investigates recognition under different observation conditions, including:

- An initial image or viewpoint
- An alternative observation of the same object or scene from a different viewpoint
- A repeated or perturbed observation used as a comparison condition

The aim is to assess whether viewpoint variation provides useful information beyond simply taking another observation.

The project also considers object visibility and occlusion when selecting and analysing observations. A different viewpoint can expose previously hidden visual evidence, but the improvement depends on the object, scene, and visibility conditions.

## Visual representation and uncertainty

The project uses pretrained visual representations, including **DINOv2 ViT-S/14**, to represent object observations and compare their visual features.

The experiments analyse recognition outcomes and uncertainty-related signals. Relevant evaluation includes:

- Recognition performance
- Whether initially incorrect predictions can be corrected by an additional observation
- Confidence or uncertainty across observation conditions
- The relationship between visibility, occlusion, and recognition behaviour

The exact experiment configuration, feature extraction steps, and evaluation procedures are documented in the notebooks.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Omeche/Uncertainty_and_active_vision.git
cd Uncertainty_and_active_vision
```

### 2. Prepare the dataset

Obtain YCB-V from the official BOP dataset resources or the dataset source used by the download utility. The repository's `download_ycbv.py` script uses the Hugging Face dataset repository `bop-benchmark/ycbv`.

The full dataset is not required for every analysis. Use the subset-preparation scripts to extract the scenes and images needed for your experiment.

### 3. Configure paths

Several preprocessing scripts contain absolute Windows paths. Replace these with paths appropriate for your environment.

For Google Colab, mount Google Drive if your dataset or prepared subset is stored there, then update the notebook paths accordingly.

### 4. Run the notebooks

Open the notebooks in Jupyter or Google Colab. Start with the dataset analysis notebook to understand the available scenes and annotations, then run the real-image or synthetic-image experiment notebook relevant to your analysis.

Some experiments depend on files produced by the preprocessing scripts. Run the corresponding preparation steps before executing the notebook cells that load those files.

## Software

The repository uses Python and common data-science and computer-vision libraries. Depending on the notebook or script, the environment may require:

- Python
- Jupyter or Google Colab
- NumPy
- Pandas
- OpenCV
- Matplotlib
- PyTorch
- scikit-learn
- DINOv2 and its model dependencies
- 7-Zip for selected archive-extraction scripts on Windows

The repository does not currently define a single pinned environment file. For reproducibility, record the package versions and runtime configuration used for your experiments.

## Reproducibility notes

- The original scripts contain local file paths that must be adapted.
- The full YCB-V dataset is not stored in this repository.
- Subset selection and train/validation splits are defined in the preprocessing scripts.
- Notebook outputs may depend on intermediate files generated locally or in Colab.
- The notebooks should be treated as the primary source for the exact experimental settings and reported results.

## Scope

This repository focuses on visual perception, object recognition, viewpoint variation, and uncertainty under occlusion. It is intended as a research and experimental codebase rather than a packaged software library.

The broader goal is to understand how an embodied AI system could use additional visual observations to make more reliable decisions when its initial view is incomplete.
