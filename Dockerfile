FROM python:3.10-slim

# Define args
ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set user
USER ${USERNAME}

ENV PATH="${PATH}:/home/${USERNAME}}/.local/bin"

COPY --chown=${USERNAME}:${USERNAME} . /home/${USERNAME}/ltv_analysis

WORKDIR /home/${USERNAME}/ltv_analysis

RUN pip install --upgrade pip && \
    bash install_dependencies.sh

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "./src/frontend/Onboarding.py"]
