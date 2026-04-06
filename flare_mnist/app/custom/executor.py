import torch
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.dxo import from_shareable, DXO, DataKind

from model import MNISTModel
from trainer import train


class MNISTExecutor(Executor):

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal):
        if task_name == "train":
            return self._train(shareable, fl_ctx, abort_signal)

        return make_reply(ReturnCode.TASK_UNKNOWN)

    def _train(self, shareable: Shareable, fl_ctx: FLContext, abort_signal):
        # 1. Unpack global weights from the DXO (numpy arrays)
        try:
            dxo = from_shareable(shareable)
        except Exception:
            return make_reply(ReturnCode.BAD_TASK_DATA)

        global_weights = dxo.data  # dict[str, np.ndarray]

        # 2. Load into model (numpy -> torch)
        torch_weights = {k: torch.as_tensor(v) for k, v in global_weights.items()}
        model = MNISTModel()
        model.load_state_dict(torch_weights)

        # 3. Train locally; returns updated state_dict (torch tensors)
        updated_weights = train(model, fl_ctx)

        # 4. Compute weight DIFF (updated - global) as numpy.
        #    InTimeAccumulateWeightedAggregator requires DataKind.WEIGHT_DIFF.
        weight_diff = {
            k: updated_weights[k].cpu().numpy() - global_weights[k]
            for k in global_weights
        }

        # 5. Wrap the diff in a DXO and return as a Shareable
        outgoing_dxo = DXO(
            data_kind=DataKind.WEIGHT_DIFF,
            data=weight_diff,
            meta={"NUM_STEPS_CURRENT_ROUND": 1}
        )
        return outgoing_dxo.to_shareable()
