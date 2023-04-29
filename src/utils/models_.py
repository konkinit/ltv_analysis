import os
import sys
import plotly.graph_objects as go
from typing import List, Tuple
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import (
    RawFeatures
)


_color = {
    "green": (0, 238, 0),
    "yellow": (205, 205, 0),
    "red": (255, 0, 0)
}


def colorRGB(
        rgb_: Tuple[int],
        *args) -> Tuple[int]:
    if args:
        return (
            rgb_[0],
            rgb_[1],
            rgb_[2],
            args[0]
        )
    return rgb_


def color_features(
        color: str,
        alpha: float) -> List[str]:
    return [
        f"rgb{colorRGB(_color[color])}",
        f"rgba{colorRGB(_color[color], alpha)}",
        f"rgba{colorRGB(_color[color], alpha)}"
    ]


def plot_(
        customer_id,
        customer_history,
        T_,
        p_alive_xarray,
        status_study_time_color,
        max_p_alive_,
        min_p_alive_,
        fig_dim,
        *args) -> None:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=customer_history[RawFeatures.T],
            y=p_alive_xarray.mean(("draw", "chain")),
            line_shape='spline',
            line=dict(color=color_features(
                                status_study_time_color,
                                0.4
                                )[0]),
            name="alive probability"
        )
    )
    fig.add_trace(
        go.Scatter(
                x=list(
                    customer_history[RawFeatures.T]
                    )+list(
                        customer_history[RawFeatures.T][::-1]
                    ),
                y=list(max_p_alive_)+list(min_p_alive_[::-1]),
                fill='toself',
                hoverinfo='skip',
                showlegend=False,
                line_shape='spline',
                fillcolor=color_features(
                                status_study_time_color,
                                0.4
                            )[1],
                line=dict(
                            color=color_features(
                                    status_study_time_color,
                                    0.4
                                )[2]
                        )
            )
    )
    fig.update_layout(
        xaxis_title="T",
        yaxis_title="probability",
        title=f"Probability Customer {customer_id} will purchase again",
        width=fig_dim[0],
        height=fig_dim[1],
    )
    fig.add_vline(
        x=T_,
        line_width=3,
        line_dash="dash",
        line_color="red",
        annotation_text="Instant t"
    )
    fig.add_vline(
        x=customer_history[RawFeatures.recency].iloc[0],
        line_width=3,
        line_dash="dash",
        line_color="black",
        annotation_text="Purchase"
    )
    if args:
        fig.add_vline(
            x=customer_history[RawFeatures.recency].iloc[-1],
            line_width=3,
            line_dash="dash",
            line_color="black",
            annotation_text="Purchase"
        )
    fig.show()
