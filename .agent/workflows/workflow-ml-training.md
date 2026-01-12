---
description: Workflow for ML Model Training with PyTorch
---

1. **Data Preparation**

    Structure your dataset class.

    ```python
    import torch
    from torch.utils.data import Dataset, DataLoader

    class CustomDataset(Dataset):
        def __init__(self, data, labels):
            self.data = torch.tensor(data).float()
            self.labels = torch.tensor(labels).long()

        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            return self.data[idx], self.labels[idx]
    ```

2. **Model Definition**

    Define neural network architecture.

    ```python
    import torch.nn as nn

    class SimpleNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(10, 64)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(64, 2)
        
        def forward(self, x):
            x = self.relu(self.fc1(x))
            return self.fc2(x)
    ```

3. **Training Setup**

    Initialize training components.

    ```python
    # Hyperparameters
    LR = 0.001
    BATCH_SIZE = 32
    EPOCHS = 10

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SimpleNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    ```

4. **Training Loop**

    Execute the training process.

    ```python
    model.train()
    for epoch in range(EPOCHS):
        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
        print(f'Epoch {epoch}: Loss {loss.item():.4f}')
    ```

5. **Evaluation**

    Validate model performance.

    ```python
    model.eval()
    correct = 0
    with torch.no_grad():
        for data, target in val_loader:
            output = model(data.to(device))
            pred = output.argmax(dim=1)
            correct += pred.eq(target.to(device)).sum().item()

    print(f'Accuracy: {100 * correct / len(val_dataset)}%')
    ```

6. **Save Model**

    Export artifacts for inference.

    ```python
    torch.save(model.state_dict(), 'best_model.pth')
    ```

// turbo
7. **Verification (Optional)**

    Run training script if available.

    ```bash
    # Example assuming script exists
    python src/train.py --epochs 1
    ```
