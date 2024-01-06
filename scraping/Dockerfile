FROM jupyter/base-notebook:python-3.11

USER $NB_USER

RUN conda install --quiet --yes \
    country_converter \
    folium \
    lxml \
    pandas==2.1.4 \
    selenium==4.11.2 \
    psycopg2 && \
    conda clean --all -f -y 
#    && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"