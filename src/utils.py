import os
import sys
import s3fs
from datetime import datetime
from numpy import full, arange
import plotly.graph_objects as go
from pandas import (
    read_csv,
    DataFrame
)
from typing import Union, Tuple, List
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import (
    RawFeatures
)


def datetime_formatting(
        df_transaction_: DataFrame,
        flag: bool = False,
        input_dt_format: str = '%d/%m/%Y %H:%M',
        output_dt_format: str = '%Y-%m-%d %H:%M') -> DataFrame:
    df_transaction = df_transaction_.copy()
    if flag:
        return df_transaction
    df_transaction[
        RawFeatures.TRANSACTION_DATE
        ] = df_transaction[
                RawFeatures.TRANSACTION_DATE
                ].apply(
                    lambda x: datetime.strptime(
                        x,
                        input_dt_format
                        ).strftime(output_dt_format) if x == x else x)
    return df_transaction


def import_from_S3(
        endpoint: str,
        bucket: str,
        path: str,
        key_id: str,
        access_key: str,
        token: str) -> DataFrame:
    """
    Connect to anS3 bucket and get data
    """
    fs = s3fs.S3FileSystem(
            client_kwargs={'endpoint_url': endpoint},
            key=key_id,
            secret=access_key,
            token=token)

    return read_csv(
                fs.open(f"{bucket}/{path}/online_retail_data.csv"),
                encoding='unicode_escape'
            )


def import_from_local(path) -> DataFrame:
    return read_csv(
                path,
                encoding='unicode_escape'
            ).set_index("Customer_ID")


def get_customer_history_data(
        data_summary: DataFrame,
        customer_id: Union[int, float, str],
        n_period_: int) -> Tuple[int, DataFrame]:
    T_ = int(data_summary.loc[customer_id][RawFeatures.T])
    frequency_ = int(data_summary.loc[customer_id][RawFeatures.frequency])
    recency_ = int(data_summary.loc[customer_id][RawFeatures.recency])
    n_period = int(T_ - recency_ + 2 + n_period_)
    df_ = DataFrame(
                dict(
                    Customer_ID=full(
                                n_period,
                                customer_id,
                                dtype="int"
                            ),
                    frequency=full(
                                n_period,
                                frequency_,
                                dtype="int"
                            ),
                    recency=full(
                                n_period,
                                recency_,
                                dtype="int"
                            ),
                    T=(arange(recency_-1, T_+n_period_+1)).astype("int"),
                ))
    df_.columns = [
        RawFeatures.CUSTOMER_ID,
        RawFeatures.frequency,
        RawFeatures.recency,
        RawFeatures.T
    ]
    return T_, df_


def get_customer_whatif_data(
        data_summary: DataFrame,
        customer_id: Union[int, float, str],
        n_period: int,
        T_future_transac: int) -> Tuple[int, DataFrame]:
    assert T_future_transac <= n_period, "Future \
        transaction must be before the end of future window"
    T_, history_ = get_customer_history_data(
                    data_summary,
                    customer_id,
                    n_period
                )
    new_transac_time = history_[
        history_["T"] == T_
        ].index.values[0] + T_future_transac
    history_[RawFeatures.frequency].iloc[new_transac_time:] += 1
    history_[RawFeatures.recency].iloc[new_transac_time:] = history_[
        RawFeatures.T].iloc[new_transac_time] - 0.01
    return T_, history_


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
