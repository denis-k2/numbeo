FROM jupyter/base-notebook

USER $NB_USER

RUN conda install --quiet --yes \
    country_converter \
    folium \
    lxml \
    pandas \
    psycopg2 && \
    conda clean --all -f -y 
#    && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"