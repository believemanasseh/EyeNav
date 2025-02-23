
#  EyeNav – Eye Navigation Extension  

**EyeNav** is an innovative extension that empowers individuals with motor disabilities to interact with digital devices **hands-free**. Using an AI-powered eye-tracking system, EyeNav provides an **accessible, cost-effective, and efficient** solution for web navigation.  

---

##  Overview  

**EyeNav** enables users to control web pages through **eye movements and blinking**. The extension works with any **standard webcam** and leverages the **IBM Granite Vision Transformer** (open-source) for precise eye tracking, eliminating the need for expensive devices.  

##  The Problem  

Many people with motor impairments struggle to use digital devices. Existing alternatives have several challenges:  

1. **Expensive adaptive devices**, making them inaccessible to many users.  
2. **Inefficient voice commands**, which can be inaccurate or impractical in certain environments.  
3. **Lack of compatibility with standard webcams**, limiting access to technology.  

##  The Solution  

**EyeNav** addresses these problems by offering **intelligent eye-tracking navigation** for the web. With **eye movements and blinks**, users can:  

- **Move the cursor** by looking at different areas of the screen.  
- **Click with short or long blinks**.  
- **Scroll through web pages** by looking up or down.  
- **Use AI adaptation in real-time**, improving accuracy over time.  

##  Key Features  

 **Cursor Control via Eye Movements** – Move the cursor just by looking.  
 **Short Blink = Left Click**, **Long Blink = Right Click**.  
 **Eye Scrolling** – Scroll pages up and down using eye movements.  
 **AI-Based Adaptation** – Learns user eye patterns for better accuracy.  
 **Works with Any Standard Webcam** – No need for expensive hardware.  
 **Simple & Intuitive Interface** – The extension runs directly in the browser.  

##  Installation  

###  Requirements  
- **Google Chrome** or a compatible browser.  
- **Functional webcam**.  
- **Permission to access the camera** in the browser.  

###  How to Install  
1. **Download the extension** from the Chrome Web Store.  
2. **Install and enable** the extension in your browser.  
3. **Allow webcam access** when prompted.  
4. **Start browsing** using just your eyes!  

---

##  Benefits & Applications  

|  Area |  Benefits |
|---------|--------------|
| **Digital Accessibility** | Enables people with disabilities to use devices without touch, promoting inclusion. |
| **Process Automation** | Reduces reliance on keyboards and mice, optimizing repetitive tasks. |
| **Business Productivity** | Facilitates navigation in corporate software, improving workflow efficiency. |
| **Customer Service** | Speeds up interactions in call centers and support platforms, reducing response times. |
| **User Experience** | Provides an intuitive way to interact using only eye movements. |
| **Diverse Sectors** | Applicable in **banking, healthcare, education, manufacturing**, and more. |
| **AI Personalization** | Learns usage patterns to make the experience smoother and more adaptable. |
| **Hygiene & Safety** | Eliminates unnecessary touch interactions, ideal for hospitals and banking environments. |
| **User Privacy** | Ensures explicit consent for eye-tracking and data security. |

---

##  Future Improvements  


 **Compatibility with more browsers** beyond Chrome.  
 **Enhanced AI for improved eye-tracking accuracy**.  
 **Additional facial gesture detection** for more versatile commands.  
 **Support for glasses and contact lenses** to increase accessibility.  
 **Integration with virtual assistants**, such as Alexa and Google Assistant.
 **Create a commercial API** that allows companies to integrate eye tracking into
   their systems, helping to include employees with disabilities in the workplace.

---

   



#  Technologies Used in EyeNav  

Below is an overview of the **technologies and frameworks** that power **EyeNav**. The system is structured into different components, each responsible for a specific functionality.  

---

##  System Architecture  


![Untitled diagram-2025-02-23-204119](https://github.com/user-attachments/assets/ee205ff8-4d46-4db4-8ec5-e13dbf8368b0)








## Development

**Clone the repository:**

```bash
git clone https://github.com/believemanasseh/EyeNav.git
cd EyeNav
```

### Chrome Extension

* Download the source code from the repository.
* Go to chrome://extensions/ in your Chrome browser.
* Enable "Developer mode" in the top right corner.
* Click "Load unpacked" and select the downloaded extension folder.

### FastAPI Server

**Navigate to server directory:**

```bash
cd server
```

**Install dependencies:**

```bash
poetry install
```

**Start development server:**

```bash
fastapi dev src/app.py
```



*EyeNav represents a major step forward in digital accessibility, providing more independence and inclusion for everyone!* 
