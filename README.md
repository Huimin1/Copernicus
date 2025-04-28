This repository is used to store the files for the presentation of the Copernicus class. The files can be devided into 2 parts, one part for the Po Plain model, the other part for the small box model.

For the box domain model: 

    'copernicus.ipynb' downloads the Sentinel data for estimating Manning's roughness coefficients
    
    'manning.pfb' is the processed Manning's coefficients, the .pfb format is used in ParFlow model
    
    'ParFlow_test.py' runs a small box model for testing the heterogeneous Manning's roughness coefficient
    
    'output' folder contains the ouput files from the box domain model
    
    'plot_outputs.ipynb' plots and analyzes the outputs from the small box model

    
For the Po Plain model:

    The atmospheric forcings of the Po Plain model is very large, it cannot be uploaded to the repository, as well as my other repositories. The forcings are saved in my CFDHub account, a folder named 'huiminw' in /global-scratch/bulk_pool. The output folder is large as well, it's saved in my private repository.  
    
    '0_clm_2023.py' shows the Po Plain model with the atmospheric forcings of the year 2023
    
    'visualize_outputs.ipynb' plots and analyzes the outputs from the Po Plain model




