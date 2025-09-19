# PyTorch on Apple Silicon - PyQt6 App Setup

## Overview
To leverage Apple's Metal Performance Shaders (MPS) backend for PyTorch in a packaged PyQt6 application on macOS.

## Requirements

### System Requirements
- macOS 12.3+ (Monterey or later)
- Apple Silicon Mac (M1/M2/M3/M4)
- Python 3.9+ (3.10 or 3.11 recommended for best compatibility)

### Key Dependencies
```txt
# requirements.txt
PyQt6>=6.5.0
torch>=2.0.0  # MPS support stable since 2.0
torchvision>=0.15.0  # If using vision models
torchaudio>=2.0.0  # If using audio models
numpy<2.0  # PyTorch compatibility
pandas>=1.5.0
statsmodels>=0.14.0
pmdarima>=2.0.0
prophet>=1.1.0
xgboost>=1.7.0
lightgbm>=3.3.0
darts>=0.24.0  # Optional, for N-BEATS/TFT
plotly>=5.0.0
```

## PyTorch MPS Backend

### Detection and Initialization
```python
import torch
import platform

def setup_torch_device():
    """Setup PyTorch to use MPS on Apple Silicon, with fallback"""
    if platform.system() == 'Darwin':  # macOS
        if torch.backends.mps.is_available():
            if torch.backends.mps.is_built():
                device = torch.device("mps")
                print(f"Using Apple Metal Performance Shaders (MPS)")
                # Set memory growth to avoid OOM
                torch.mps.set_per_process_memory_fraction(0.0)  # Dynamic allocation
                return device
            else:
                print("MPS not built into PyTorch installation")
        else:
            print("MPS not available on this Mac")

    # Fallback to CPU
    device = torch.device("cpu")
    print(f"Using CPU")
    return device

# Usage
device = setup_torch_device()
model = YourModel().to(device)
data = data.to(device)
```

### MPS-Specific Considerations
```python
# 1. Memory Management - MPS has different memory patterns than CUDA
torch.mps.empty_cache()  # Clear MPS cache when needed

# 2. Some operations may not be implemented for MPS yet
try:
    result = some_operation()
except NotImplementedError:
    # Fallback to CPU for unsupported ops
    data_cpu = data.cpu()
    result = some_operation(data_cpu)
    result = result.to(device)

# 3. Mixed precision training (if needed)
from torch.cuda.amp import autocast, GradScaler
# Note: autocast works with MPS but GradScaler is CUDA-only
with autocast(device_type='mps' if device.type == 'mps' else 'cpu'):
    output = model(input)
```

## Packaging Strategy

### 1. Using PyInstaller
```bash
# Install PyInstaller
pip install pyinstaller

# Create spec file with proper hooks
pyinstaller --name MarketForecaster \
    --windowed \
    --onedir \
    --hidden-import torch \
    --hidden-import torch.mps \
    --collect-all torch \
    --collect-all prophet \
    --collect-all statsmodels \
    --copy-metadata torch \
    main.py
```

### 2. PyInstaller Spec File Modifications
```python
# MarketForecaster.spec
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include PyTorch MPS backend files
        ('venv/lib/python3.11/site-packages/torch/lib/*.dylib', 'torch/lib'),
        # Include model weights if pre-trained
        ('models/*.pth', 'models'),
    ],
    hiddenimports=[
        'torch',
        'torch.mps',
        'torch.distributions',
        'torch.nn.modules',
        'sklearn.utils._cython_blas',
        'sklearn.neighbors._typedefs',
        'sklearn.neighbors._quad_tree',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch.cuda', 'torch.backends.cuda'],  # Exclude CUDA
    noarchive=False,
)
```

### 3. Alternative: py2app (Mac-specific)
```python
# setup.py for py2app
from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['torch', 'PyQt6', 'numpy', 'pandas'],
    'includes': ['torch.mps'],
    'excludes': ['torch.cuda'],
    'frameworks': [],  # MPS uses system Metal.framework
    'plist': {
        'CFBundleName': 'Market Forecaster',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.yourcompany.marketforecaster',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '12.3',  # For MPS support
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

### 4. Alternative: Briefcase (Modern approach)
```toml
# pyproject.toml
[tool.briefcase]
project_name = "Market Forecaster"
bundle_identifier = "com.example.marketforecaster"

[tool.briefcase.app.marketforecaster.macOS]
requires = [
    "torch>=2.0.0",
    "PyQt6>=6.5.0",
]
system_requires = [
    "macOS>=12.3",  # MPS requirement
]
```

## Application Structure

### Main Application with MPS Support
```python
# main.py
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
import torch

class ModelWorker(QThread):
    """Background thread for model training/inference"""
    progress = pyqtSignal(int)
    result = pyqtSignal(object)

    def __init__(self, data, model_type='mlp'):
        super().__init__()
        self.data = data
        self.model_type = model_type
        self.device = self.setup_device()

    def setup_device(self):
        if torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")

    def run(self):
        try:
            # Move data to device
            tensor_data = torch.tensor(self.data).to(self.device)

            # Run model
            if self.model_type == 'mlp':
                model = self.create_mlp().to(self.device)
            elif self.model_type == 'nbeats':
                model = self.create_nbeats().to(self.device)

            # Training/inference here
            output = model(tensor_data)

            # Move back to CPU for GUI
            result = output.cpu().numpy()
            self.result.emit(result)

        except Exception as e:
            print(f"Model error: {e}")
            # Fallback to CPU
            self.device = torch.device("cpu")
            self.run()  # Retry on CPU

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.check_mps_availability()

    def check_mps_availability(self):
        """Check and display MPS status"""
        if torch.backends.mps.is_available():
            self.statusBar().showMessage("✓ Apple Metal acceleration available")
        else:
            self.statusBar().showMessage("Running on CPU (MPS not available)")
```

## Model Examples for Time Series

### 1. Simple MLP for Global Forecasting
```python
class GlobalMLP(torch.nn.Module):
    def __init__(self, input_size, hidden_size=64, horizon=12):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(input_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Linear(hidden_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Linear(hidden_size, horizon)
        )

    def forward(self, x):
        return self.net(x)
```

### 2. Using Darts with MPS
```python
from darts.models import NBEATSModel, TFTModel
import torch

# Configure Darts to use MPS
device = "mps" if torch.backends.mps.is_available() else "cpu"

# N-BEATS
model = NBEATSModel(
    input_chunk_length=24,
    output_chunk_length=12,
    n_epochs=100,
    torch_device_str=device,  # Use MPS
    batch_size=32,
)

# TFT
model = TFTModel(
    input_chunk_length=24,
    output_chunk_length=12,
    n_epochs=100,
    torch_device_str=device,
    batch_size=32,
)
```

## Testing MPS Performance

```python
import time
import torch
import numpy as np

def benchmark_mps():
    """Compare MPS vs CPU performance"""
    sizes = [100, 1000, 10000]

    for size in sizes:
        # Create random data
        data = torch.randn(size, 100, 50)  # batch, sequence, features

        # CPU timing
        model_cpu = GlobalMLP(50, 128, 12)
        data_cpu = data.cpu()

        start = time.time()
        with torch.no_grad():
            _ = model_cpu(data_cpu)
        cpu_time = time.time() - start

        # MPS timing (if available)
        if torch.backends.mps.is_available():
            model_mps = GlobalMLP(50, 128, 12).to('mps')
            data_mps = data.to('mps')
            torch.mps.synchronize()  # Ensure previous ops complete

            start = time.time()
            with torch.no_grad():
                _ = model_mps(data_mps)
            torch.mps.synchronize()  # Ensure computation completes
            mps_time = time.time() - start

            print(f"Size {size}: CPU={cpu_time:.3f}s, MPS={mps_time:.3f}s, "
                  f"Speedup={cpu_time/mps_time:.1f}x")
        else:
            print(f"Size {size}: CPU={cpu_time:.3f}s, MPS not available")
```

## Troubleshooting

### Common Issues and Solutions

1. **MPS not available after packaging**
   - Ensure Metal.framework is accessible
   - Don't use --onefile with PyInstaller (use --onedir)
   - Include all torch.lib/*.dylib files

2. **Memory errors on MPS**
   ```python
   # Set memory fraction
   torch.mps.set_per_process_memory_fraction(0.5)  # Use 50% of available memory

   # Clear cache periodically
   torch.mps.empty_cache()
   ```

3. **Operations not implemented for MPS**
   ```python
   def safe_operation(tensor, operation):
       try:
           return operation(tensor)
       except NotImplementedError:
           # Fallback to CPU
           cpu_tensor = tensor.cpu()
           result = operation(cpu_tensor)
           return result.to(tensor.device)
   ```

4. **App crashes on Intel Macs**
   ```python
   def get_safe_device():
       if platform.processor() == 'arm':  # Apple Silicon
           if torch.backends.mps.is_available():
               return torch.device('mps')
       return torch.device('cpu')
   ```

## Build Script
```bash
#!/bin/bash
# build_mac_app.sh

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Test MPS availability
python -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"

# Build with PyInstaller
pyinstaller MarketForecaster.spec

# Sign the app (requires Apple Developer certificate)
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" \
    dist/MarketForecaster.app

# Create DMG for distribution
hdiutil create -volname "Market Forecaster" -srcfolder dist/MarketForecaster.app \
    -ov -format UDZO MarketForecaster.dmg
```

## Performance Expectations

### On Apple Silicon (M1/M2/M3)
- **Simple MLP**: 2-5x faster than CPU
- **N-BEATS**: 3-8x faster than CPU
- **TFT**: 3-6x faster than CPU
- **Memory**: MPS unified memory architecture means less copying

### Model Training Times (300 series, 60 points each)
- **CPU**: 5-15 minutes
- **MPS**: 1-3 minutes
- **Benefits**: Real-time scenario updates possible

## Distribution Checklist

- [ ] Test on Intel Mac (CPU fallback)
- [ ] Test on M1/M2/M3 Macs (MPS acceleration)
- [ ] Verify all dependencies included
- [ ] Sign with Apple Developer certificate
- [ ] Notarize for Gatekeeper approval
- [ ] Test fresh install on clean system
- [ ] Verify MPS acceleration working in packaged app