![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&width=1000&height=200&section=header&text=PRAEDICO&fontSize=30&fontColor=black)


<!-- header is made with: https://github.com/kyechan99/capsule-render -->

[Briggs Lalor](https://www.linkedin.com/in/briggsclalor/) [<img src="https://cdn2.auth0.com/docs/media/connections/linkedin.png" alt="LinkedIn -  Briggs Lalor" width=15/>](https://www.linkedin.com/in/briggsclalor/)
[Ken Lee](https://www.linkedin.com/in/kenkwlee) [<img src="https://cdn2.auth0.com/docs/media/connections/linkedin.png" alt="LinkedIn -  Ken Lee" width=15/>](https://www.linkedin.com/in/kenkwlee)
[Stephane Maysn](https://www.linkedin.com/in/stephane-masyn-35b16817a/) [<img src="https://cdn2.auth0.com/docs/media/connections/linkedin.png" alt="LinkedIn -  Staphane Masyn" width=15/>](https://www.linkedin.com/in/stephane-masyn-35b16817a/)
[John Sung](https://linkedin.com/in/john-sung-3675569) [<img src="https://cdn2.auth0.com/docs/media/connections/linkedin.png" alt="LinkedIn -  John Sung" width=15/>](https://linkedin.com/in/john-sung-3675569/)
                                                             
![numisma](images/numisma.PNG)

---

### Table of Contents

* [Executive Summary](#executive-summary)
* [Requirements](#requirements)
* [Data](#data)
* [Visualization](#visualization)
* [User Experience](#user-experience)
* [Web Sources](#web-sources)
* [License](#license)  

---

## Executive Summary

Fear of change, metathesiophobia, is a phobia that causes people to avoid changing their circumstances due to being extremely afraid of the unknown. That unknown we are referencing is the crytocurrency market. And although we have seen volitility in the cryptocurrency space, we have also witnessed impressive growth as investors feel more confident in the blockchain ecosystem. An example of this is Bitcoin, the largest of the cryptocurrencies. Bitcoin has had returns of 88% in 2019, 302% in 2020 and nearly 60% in 2021. Bitcoin's market cap has already exceeded $700 Billion. Nonetheless, Investors are still apprehensive of investing in something they don’t understand.

As a result, we have created a new tool that allows our investors to invest in the crypto market using our research and blockchain technology. In our interactive application, the investor can invest in three options. This app will give you the option of yield farm index [FarmDex], metaverse index [MetDex]and large coin index [VentiDex] using our asset allocation model. You will also be able to connect your metamask wallet to purchase the invesment and take a realtime photo to attach to Please enjoy the experience and please choose wisely!



Now that we explained why we developed of our application, let's go into the methodology behind the building of the app. In our application, we used the CRISP-DM Methodology to help our team stay organized to come up with a solution that predicts the winner of the Super Bowl LVI. By reviewing the code, you will come to know where and how we came up with our secret sauce called the Praedico. 

In our MVP, we have created a user friendly dashboard using Steamlit to help users view stats, summary and overall predicitons using interchangeable machine learning models. As we continue to work on our application, we will look to include other sports, the ability to...

1) Place a wager and add additional features like betting odds

2) Add loops to automate  most efficient model,

3) Add features to include injury status, QB efficiency and weather components

4) Once games are played, we will automate scores from the internet to place the incorrect teams to re-run the model

...to enhance our user experience. Please enjoy and may the Praedico be with you!


---

## Requirements

Installation instructions
$ pip install yfinance --upgrade --no-cache-dir
$ pip install streamlit-aggrid
$ Pip install tweepy
This project leverages python 3.7 Streamlit and scikit-learn.

A [conda](https://docs.conda.io/en/latest/) environment with liabraries listed below and [Jupyter Notebook/Lab](https://jupyter.org/) are required to run the code.

The following library was used:

1. [Scikit Learn](https://scikit-learn.org/stable/index.html) - Scikit Learn or Sklearn is one of the most used Python libraries for Data Science, along with others like Numpy, Pandas, Tensorflow, or Keras.

2. [Streamlit](https://streamlit.io/) - Streamlit turns data scripts into shareable web apps in minutes.


Install the following librarie(s) in your terminal...

    pip install -U scikit-learn
    pip install streamlit
 
---

## Data



---

## Visualization


### Using offensive and deffensive categories to create training Set
![training set](images/create_training_set.PNG)

### Evaluating the samples of Mean Abolute Error of four models shown and using the best mean absolute error 
![super model](images/super_model.PNG)

### Dataframe Creation
![data frame](images/data_frame_creation.PNG)

### Showing the scores being predicted 
![score_predictor](images/back_end_score_predictor.PNG)

## Front end application images

### Select the team for analysis
![Choose Team](images/choose_team_annalysis.PNG)

### Choose the model
![Choose Model](images/choose_model.PNG)

### Run the model for projection
![Run Praedico](images/click_run_praedico.PNG)

### The WINNER is... 
![Winner Praedico](images/winner_prediction.PNG)

---

## User Experience

Go to the Anaconda Prompt to launch JupyterLab by typing Jupyter Lab. To use this application simply clone the repository and run the NFL_Dashboard.py in your Jupyter Lab. Open a terminal and input streamlit run NFL_Dashboard.py or simply choose from the two options below.


Please experience Praedico for yourself. Choose between the following... 

1) CLICK 

2) SCAN the QR Reader using the camera from your phone. 

![QR_Reader](images/qr_reader.PNG)


---

## Web Sources



---


## License

MIT

---


