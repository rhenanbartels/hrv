---
title: 'HRV: a Pythonic package for Heart Rate Variability Analysis'
tags:
  - Python
  - cardiac autonomic system
  - heart rate variability 
authors:
  - name: Rhenan Bartels
    orcid: 0000-0002-6088-2186
    affiliation: "1"
  - name: Tiago Peçanha
    orcid: 0000-0003-4968-5525
    affiliation: "2"
affiliations:
  - name: Pulmonary Engineering Laboratory, Biomedical Engineering Program, Federal University of Rio de Janeiro, Rio de Janeiro, Brazil
    index: 1
  - name: Faculty of Medicine, University of São Paulo, Brazil
    index: 2
date: 25 October 2019
bibliography: paper.bib
---

# Summary
Heart rate variability (HRV) is a non-invasive tool to assess the cardiac autonomic integrity and cardiovascular homeostasis [@electrophysiology1996heart]. HRV quantifies the instantaneous variations in the RR intervals (RRi), which is produced by the balanced action of the parasympathetic and sympathetic branches of the autonomic nervous system (ANS) over the sinoatrial (SA) node, and modulated by different physiological inputs (e.g., respiration, blood pressure, temperature, emotions, etc) [@malik1990heart]. Specifically, the parasympathetic activation produces fast and short-lasting bradycardia, which results in high-frequency oscillations (i.e., 0.15 - 0.40 Hz) in heart rate. On the other hand, sympathetic activation produces slower and longer-lasting variations in heart rate, which results in low-frequency (i.e., ~ 0.1 Hz) oscillations in heart rate.  

Increased HRV indicates a predominance of the parasympathetic over the sympathetic activation in the SA node, and indicates enhanced cardiac autonomic flexibility and improved overall health [@malik1990heart]. Conversely, a reduced HRV is usually accompanied by sympathetic dominance and suggests increased rigidity and loss of control of the ANS to the cardiovascular system, which is a sign of disease vulnerability [@malik1990heart]. For instance, a reduced SDNN (i.e., standard deviation of RR intervals, a simple statistical-based time domain  index of HRV) has been shown to overperform traditional cardiovascular risk parameters in predicting mortality in a cohort of heart failure patients [@nolan1998prospective]. A reduced HRV has also been linked with metabolic dysfunction [@weissman2006power], increased inflammation [@sajadieh2004increased], depression [@sgoifo2015autonomic],  psychiatric disorders [@degiorgio2010rmssd], sleep disturbance [@burton2010reduced], among others. Based on this wide prognostic utility, the interest in approaches to evaluate HRV has shown an exponential growth in different medicine specialties and research fields in the recent years.  

HRV is routinely assessed using linear methods, through the calculation of different indices either in time- or frequency-domain. Time-domain consists of a collection of statistical metrics, such as the average value of RRi (mRRi), the standard deviation of RRi (SDNN; the NN stands for natural or sinusal intervals), the standard deviation of the successive differences (SDSD), the number or percentage of RRi longer than 50ms (NN50 and pNN50) and the root mean squared of successive difference in adjacent RRi (RMSSD - equation 1) [@electrophysiology1996heart].  Each of these indices quantifies different facets of the HRV, which are promoted by different autonomic sources. SDNN quantifies overall variability behind HRV, which is produced by both parasympathetic and sympathetic branches. NN50, pNN50, and RMSSD quantify beat-to-beat HRV, which is produced predominantly by the parasympathetic action in the heart. 

$$RMSSD = \sqrt{\frac{1}{N-1}\sum_{j-1}^{N-1}(RRi_{j} - RRi_{j+1})^2}$$ - Equation 1

where $N$ is the count of RRi values and $RRi_{j}$ is the jth RRi value.

The frequency-domain analysis quantifies the extent of contribution of each frequency component to the overall heart rate fluctuation (Figure 2). The main frequency components are the VLF (i.e., very low frequency; $<$ 0.04 Hz); LF (low frequency; 0.04-0.15 Hz) and the HF (i.e., high frequency; 0.15-0.40 Hz). The HF component is coupled with the respiratory fluctuation (i.e., respiratory sinus arrhythmia) and is produced by the parasympathetic modulation on the heart. The LF is mainly coupled with variations in the blood pressure (i.e.,  Mayer waves), and is thought to represent the modulation of both parasympathetic and sympathetic branches on the heart. The VLF does not have a defined physiological source, but it may involve alterations in heart rate produced by hormones and body temperature [@electrophysiology1996heart]. 

Roughly, frequency domain analysis involves the calculation of the spectral energy content of each frequency component through a power spectral density (PSD) estimation. Several methods have been developed to perform the PSD estimation and they are generally divided into two categories that provide comparable results: non-parametric and parametric methods, each with respective pros and cons [@electrophysiology1996heart]. The Welch periodogram [@welch1967use] is a non-parametric approach based on the Fourier Transform and consists of the average of several PSD estimations on different segments of the same RRi series, which is an important approach to reduce the spectral estimation variability [@welch1967use]. On the other hand, the autoregressive technique is the most widely used parametric method to estimate the spectral components of the HRV signal [@berntson1997heart]. The PSD estimation with the autoregressive method consists of a parametric representation of the RRi series and the frequency response of the estimated model. From the estimated PSD, generally, the following indices presented in Table 1 are calculated.

| Variable | Units | Frequency Band |
| -------- | ----- | -------------- |
| Total Power | ms<sup>2</sup> | 0 - 0.4 Hz |
| VLF | ms<sup>2</sup> | $<$ 0.04 Hz |
| LF | ms<sup>2</sup> | 0.04 - 0.15 Hz |
| HF | ms<sup>2</sup> | 0.15 - 0.4 Hz |
| LF/HF | | |
| LF<sub>n.u</sub> | normalized units $\frac{LF}{Total Power - VLF}$ | |
| HF<sub>n.u</sub> | normalized units $\frac{HF}{Total Power - VLF}$ | |

Non-linear indices are also frequently used to extract information from the ANS based on the heart rate fluctuations patterns. The Poincaré ellipse plot belongs to the non-linear methods and consists of a diagram in which each RRi is plotted as a function of the previous RRi value [@berntson1997heart]. In addition to the visual information about the RRi scatter given by the plot, two indices are extracted from this diagram: SD1 and SD2. The former reflects the short term fluctuations of the heart rate, and for this reason is highly correlated with the RMSSD, pNN50 and HF indices, while the latter reflects both short and long terms of the fluctuation of the heart rate and correlates with SDNN and LF indices. Additionaly, the SD1 index represents the standard deviation spread orthogonally to the identity line (y=x) and it is the ellipse width, whereas the SD2 index represents the standard deviation spread along the identity line and specifies the length of the ellipse. At the end of the following section, the Poincaré plot of a given RRi series is depicted using the module presented in the current article. 

The calculation of the SD1 and SD2 can be derived from SDSD and SDNN values as shown by equations 2 and 3 below:

$$SD1 = \sqrt{2SDNN^{2} - 2SD2^{2}}$$ - Equation 2

$$SD2 = \sqrt{2SDNN^{2} - \frac{1}{2}SDSD^{2}}$$ - Equation 3

There are several software packages written in many different programming languages that offer functions to work with RRi signals. Some of them have a command-line interface [@rodriguez2008rhrv] and others offer a user's interface to improve the interaction with the RRi series and the analyses  [@tarvainen2014kubios,@bartels2017sinuscor]. 
Specifically for Python, there is also open-source packages available and ready to work on HRV analisys, such as [hrvanalysis](https://github.com/Aura-healthcare/hrvanalysis), pyhrv [@Gomes2019], and [heartpy](https://github.com/paulvangentcom/heartrate_analysis_python). Although these modules do a great work offering many of the most widely used techniques to deal with tachograms and to extract relevant information from HRV signals, their functions interface (API) relies on RRi signals stored as Python iterable or numpy arrays and is based mostly on the procedural programming paradigm. 

The `hrv` is a simple and open-source Python module that comes with the most common techniques for filtering, detrending and extracting information about the ANS from the RRi signals without losing the power and flexibility of a native Python object and a numpy arrays [@numpy]. It brings the necessary methods to work with a tachogram encapsulated in a Python class. In other words, once an RRi class is instantiated there are several methods available for visualization, descriptive statistics, slicing the signal in shorter segments, and displaying the metadata of the series.

With many software available to work with HRV analysis, the main reason why the `hrv` module is being developed is to improve and simplify the interaction with an RRi series with idiomatic Python code, closer to the native objects of this language. The object-oriented approach offered by the present module allows a strong relation between the RRi series and its methods, especially regarding time information. With a class representing and encapsulating the RRi object, each RRi value is bound to its respective time information, and therefore, after actions like slicing and filtering, the RRi series still keeps track of its information. Additionally, the instance's properties help to keep the state of the RRi series, informing if it is already detrended and/or resampled.

The following sections present the basic workflow with an RRi series and gives a better overview of the functionalities available in the `hrv` module, starting with reading a file containing a tachogram, visualizing the given RRi series, dealing with noise filtering and detrending and, finally, calculating the time/frequency domain and non-linear HRV indices.

# Basic Usage

This section presents a non-exhaustive walkthrough of the features offered by the ```hrv``` module. To have access to the source code and more usage examples, please refer to the [software repository](https://github.com/rhenanbartels/hrv) and the complete [documentation](https://hrv.readthedocs.io/en/latest/index.html).

Once the RRi series is created in Python using the ```hrv.io``` submodule, which supports text, CSV and hrm (Polar<sup>TM</sup>) files, or from any Python iterable (i.e lists, tuples, etc), an RRi instance with the necessary methods to implement the Python iterable pattern is created. With the RRi object it is possible to iterate (i.e ```[r for r in rri_series]```), search for a value at a given index (i.e ```rri_series[0]```), and slice the tachogram (i.e ```rri_series[5:10]```). As the RRi class also implements some of the behaviors of the numpy array [@numpy], it is possible to perform math operations with the tachogram, i.e: ```rri_series / 1000```.

The RRi class also has methods for basic statistical metrics calculation, such as average, standard deviation, min and max, and others. In order to access a complete Python dictionary containing all available statistical metrics of an RRi instance, it is possible to call the ``describe`` method. Features for visualization are also present in the RRi class. In order to visualize the time series represented by the RRi series, the ``plot`` method can be called. The visualization of the histograms showing the distributions of RRi or heart rate time series is also possible with the method ``hist``.
`

## Read a file containing RRi values and visualising it 

The following code snippet shows how to read a RRi series from a single column CSV file and plot the respective series with black lines.

```python
from hrv.io import read_from_csv  

rri = read_from_csv('path/to/file.csv')

fig, ax = rri.plot(color='k')

```

![RR intervals of a young subject at rest condition produced with the ```plot``` method from the RRi class.](rri_series.png)

To retrieve statistical properties of a RRi series the method ```describe``` can be invoked:

```python
desc = rri.describe()

desc
----------------------------------------
                   rri          hr
----------------------------------------
min             750.00       66.30
max             905.00       80.00
mean            805.50       74.78
var            2646.25       20.85
std              51.44        4.57
median          805.00       74.54
amplitude       155.00       13.70


print(desc['std'])
{'rri': 51.44171459039833, 'hr': 4.5662272355549725}
```

## Pre-processing
### Filtering the RRi series

In some cases and for many different reasons, the tachogram may present with movement artifacts or undesired RRi values, which may jeopardize the analysis results. One way to deal with this scenario is to apply filters to the RRi series. For this reason, the hrv package offers three lowpass filters for noise removal: moving average, which given an order value $N$, replaces every RRi value by the average of its $N$ neighbors values;  the moving median, which works similarly to the moving average filter, but apply the median function; and the quotient filter [@piskorski2005filtering], that removes the RRi values which the ratio with its adjacent RRi are greater than 1.2 or smaller than 0.8.

```python
from hrv.filters import moving_median, quotient

filt_rri_median = moving_median(rri, order=3)
filt_rri_quotient = quotient(rri)

filt_rri_median.plot(ax=ax)
filt_rri_quotient.plot(ax=ax)
```

![The left panel shows the original RRi (blue line) and after filtering with a moving median filter with order equal to 3 (orange line).  The left panel depicts the original RRi (blue line) and after filtering with a quotient filter (orange line). This picture was created using the ``plot``` method from the ```RRi``` instance.](rri_filtered.png)

### Detrending the RRi series

Although the very-low-frequency components of the PSD function might have useful information, they are generally removed from the RRi signals before the frequency-domain analysis is performed. This pre-processing step before the frequency-domain analysis is important to remove intrinsic slow trends that are present in the HR fluctuation. This non-stationary behavior may contaminate the overall dynamic of the RRi series and influence the results, especially the VLF and LF measures [@tarvainen2002advanced]. For this reason, several methods have been developed to extract the frequency components responsible for the non-stationary behavior of the RRi series. 

Among the methods available in the literature for detrending the RRi series, the `hrv` module offers the polynomial detrend, which consists of the subtraction of an Nth degree polynomial from the RRi signal, where N is smaller than the length of the tachogram. It also offers the Smoothness Priors method [@tarvainen2002advanced], which is widely used in HRV analyses and acts as a lowpass filter to remove complex trends from the RRi series. Finally, the `hrv` module also offers a detrending method that uses the Savitsky-Golay lowpass filter to remove low-frequency trends from the RRi series.

```python
from hrv.detrend import polynomial_detrend, sg_detrend
from hrv.sampledata import load_rest_rri

rri = load_rest_rri()

detrended_rri_poly = polynomial_detrend(rri, degree=1)
detrended_rri_sg = sg_detrend(rri, window_length=51, polyorder=3)

detrended_rri_poly.plot()
detrended_rri_sg.plot()
```

![The left panel shows the original RRi (blue line) and after detrending with polynomial function with degree 1 (black line).  The left panel depicts the original RRi (blue line) and after detreding with a Savitsky-Golay lowpass filter (black line).](rri_detrended.png)


## Analyses
### Time Domain 

In order to calculate the time-domain indices, the function ```time_domain``` can be imported from the submodule ```hrv.classical``` and applied to any Python iterable containing the RRi series including the RRi instance from the module presented in this article.

```python
from hrv.classical import time_domain

results = time_domain(rri)
print(results)

{'mhr': 66.528130159638053,
 'mrri': 912.50302419354841,
 'nn50': 337,
 'pnn50': 33.971774193548384,
 'rmssd': 72.849900286450023,
 'sdnn': 96.990569261440797
 'sdsd': 46.233829821038042}
```

### Frequency Domain

Similarly to the ```time_domain``` function, to calculate the frequency-domain indices, the ```frequecy_domain```, which is also placed in the ```hrv.classical``` submodule, can be used. The ```frequency_domain``` function present in the ```hrv``` module takes care of the pre-processing steps:  the detrending of the RRi series (which the default is a linear function, but can be any custom Python function), interpolation using cubic splines (also accepts linear interpolation) and resampling at a given frequency, the default is 4 Hz.

When Welch’s method is selected, a window function (default: hanning), the number of RRi values per segment and the length of superposition between adjacent segments can be chosen. When the AR method is selected, the order of the model (default 16) can be set.

The area under the curve of each frequency range in the estimated PSD is calculated using the trapezoidal method. As a default, the hrv module uses the frequencies cutoffs shown in Table 1 to limit the integration range of each frequency domain indices, however, it is possible to set the frequency range of VLF, LF, and HF  in the ```frequency_domain``` function call.

```python
from hrv.classical import frequency_domain

results = frequency_domain(
    rri=rri,
    fs=4.0,
    method='welch',
    interp_method='cubic',
    detrend='linear'
)
print(results)

{'hf': 1874.6342520920668,
 'hfnu': 27.692517001462079,
 'lf': 4894.8271587038234,
 'lf_hf': 2.6110838171452708,
 'lfnu': 72.307482998537921,
 'total_power': 7396.0879278950533,
 'vlf': 626.62651709916258}
```

![Power Spectral Density of a RRi series estimated with the Welch's method.](psd.png)

### Non-linear
Finally, among the non linear metrics, ```hrv``` module offers SD1 and SD2, which can be calculated with the ```non_linear``` function from the ```hrv.classical``` submodule.

```python
from hrv.classical import non_linear

results = non_linear(rri)
print(results)

{'sd1': 51.538501037146382,
 'sd2': 127.11460955437322}
```

The respective Poincaré plot of a given RRi series can be depicted with the `poincare_plot()` method, as follows:

```python
rri.poincare_plot()
```

![Poincaré plot of a given RRi series.](poincare.png)

# Dependencies

The ```hrv``` package depends on the following modules: numpy [@numpy], matplotlib [@hunter2007matplotlib], scipy [@scipy] and spectrum [@cokelaer2017spectrum].

# Acknowledgements

The authors are grateful to CAPES (Coordenadoria de Aperfeiçoamento de Pessoal de Nível Superior), FAPERJ (Fundação de Amparo à Pesquisa do Estado do Rio de Janeiro), FAPESP (2016/23319-0 - Fundação de Amparo à Pesquisa do Estado do São Paulo) and CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico) for financial support. We are also grateful to Wilson Mello a.k.a Bakudas for creating the nice logo of the ```hrv``` module.

# References
