## Commonly used scripts

This repo contains scripts for some of the common tasks.

To create this environment,

```
1. conda create --name myenv
```

You can change the name of the environment by modifying the first line, `name: geo-scripts` to something else if you prefer, else it will create conda environment with that name.

Next, create the environment using

```
2. conda env create -f environment.yml
```

You can also do `conda env create -f environment.yml -n custom_name` if you want to have a custom name without changing the `environment.yml` file.

Once the environemtn is installed, activate it using (replace with your environment name)

```
3.conda activate your_env_name
```


### Usage

1. `python tiff-2-tiles.py -i="/Users/bbhandar/Downloads/nlcms/tiffs" -o="/Users/bbhandar/Downloads/nlcms/tiles/" -t=512`

You can do `python name-of-script.py -h` to understand the input, output and parameters relating to the script.
