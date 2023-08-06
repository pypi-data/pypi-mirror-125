# runthis ![tests](https://github.com/microprediction/runthis/workflows/tests/badge.svg) ![deploy-pypi](https://github.com/microprediction/runthis/workflows/deploy-pypi/badge.svg)
Tired of your data science experiments becoming a mess? 
Don't want to pay $20,000 a year for a data science platform?
Here's your poor man's version. 


### Usage
Name your experiment files like this: 

       my_function?n=5&d=cat&init=[0.2,0.2,0.2].py
    
Then your experiment file looks like this: 


        if __name__=='__main__':
            import os
            kwargs = parse_kwargs(__file__.split(os.path.sep)[-1])
            my_experiment(**kwargs)


This way what you do in the experiment never gets out of sync with the code. 


### Int, Float
Just call the experiment file 

    my_function?n=int:5&d=cat&init=[float:0.2,float:0.2,float:0.2].py

instead

### Example 
See [here](https://github.com/microprediction/runthis/blob/main/examples/mean_info_max_shgo%3Fn%3D5%26d%3Dcat%26init%3D%5B0.2%2C0.2%2C0.2%5D.py)

![](https://github.com/microprediction/runthis/blob/main/images/run_this.png)
