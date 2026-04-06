import logging
import os
import torch
import torch.optim as optim
from torchvision import datasets, transforms
from nvflare.apis.fl_context import FLContext
from model import MNISTModel
 
logger = logging.getLogger(__name__)
 
# Hyperparameters
_EPOCHS = 2
_BATCH_SIZE = 32
_LR = 0.01
 
def train(model: MNISTModel, fl_ctx: FLContext) -> dict:
    # 1. Select the device (cuda if available, otherwise cpu)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Training on device: {device}")

    # 2. Move the entire model to the selected device
    model.to(device)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    transform = transforms.ToTensor()
    dataset = datasets.MNIST(data_dir, train=True, download=True, transform=transform)
    
    # 3. Optimization: pin_memory=True speeds up data transfer to GPU
    loader = torch.utils.data.DataLoader(
        dataset, batch_size=_BATCH_SIZE, shuffle=True, pin_memory=torch.cuda.is_available()
    )

    optimizer = optim.SGD(model.parameters(), lr=_LR)
    loss_fn = torch.nn.CrossEntropyLoss()

    model.train()
    for epoch in range(_EPOCHS):
        running_loss = 0.0
        for x, y in loader:
            # 4. Move each batch of data (inputs and labels) to the device
            x, y = x.to(device), y.to(device)
            
            optimizer.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        avg_loss = running_loss / len(loader)
        logger.info(f"Epoch {epoch + 1}/{_EPOCHS} — avg loss: {avg_loss:.4f}")

    # 5. Move the model back to CPU before returning the state_dict 
    # This ensures compatibility with NVFlare's serialization/aggregation
    model.to("cpu")
    return model.state_dict()