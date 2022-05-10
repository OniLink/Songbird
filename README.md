# Songbird
Code for the 2021-2022 Capstone project for the Songbird Heartbeat Project

**Period Slider:**
This slider adjusts the period where bird heartbeats are captured. 
It will enforce a minimum period and acts as a basic lowpass filter. 
The higher the value of the slider, the more high frequency peaks get removed, but there is more of a chance of a returning a false bpm. 
The lower the value of the slider, the more high frequency peaks get through.   
**Prominence:**
This slider adjusts what the code looks for in the difference between the highest peak and the median line, 
this helps the code pick out the peaks with more ease. 
A higher prominence is more selective on which peaks get counted and picks out the higher peaks in the data, 
and a lower prominence accounts for variation between peak loudness. i.e. when the data isn't as well filtered.   
**Tip:**
A recommendation for sifting through the data, is that when the data looks irregular
and causes a large offset from expected values, it is best to examine a shorter interval of time.
For most accurate heartbeat data, these sliders should be set to the smallest values that adhere to closest known accuracy.
