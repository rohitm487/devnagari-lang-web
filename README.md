# देवनागरी Programming Language Web IDE

देवनागरी प्रोग्रामिंग भाषा के लिए एक ऑनलाइन IDE, जो आपको Pyiodide का उपयोग करके सीधे अपने ब्राउज़र में कोड लिखने और चलाने की अनुमति देता है।

## विशेषताएं (Features)

- 🌐 ब्राउज़र-आधारित निष्पादन - कोई इंस्टॉलेशन आवश्यक नहीं
- 📝 सिंटैक्स-हाइलाइटेड कोड एडिटर
- 🎯 रीयल-टाइम कोड निष्पादन
- 📚 बिल्ट-इन कोड उदाहरण
- 🎨 आधुनिक, रेस्पॉन्सिव UI
- 💻 क्रॉस-प्लेटफॉर्म संगतता

## त्वरित प्रारंभ (Quick Start)

1. लाइव डेमो पर जाएं [rohitm487.github.io/devnagari-lang-web](https://rohitm487.github.io/devnagari-lang-web)
2. सीधे अपने ब्राउज़र में देवनागरी में कोडिंग शुरू करें!

## स्थानीय इंस्टॉलेशन (Local Installation)

### विधि 1: Git का उपयोग करके (Recommended)

1. रिपॉजिटरी को क्लोन करें:
   ```bash
   git clone https://github.com/rohitm487/devnagari-lang-web.git
   cd devnagari-lang-web
   ```

2. स्थानीय सर्वर शुरू करें:
   ```bash
   python3 -m http.server 8000
   ```

3. अपने ब्राउज़र में `http://localhost:8000` पर जाएं

### विधि 2: सीधा डाउनलोड

1. [रिलीज पेज](https://github.com/rohitm487/devnagari-lang-web/releases) पर जाएं
2. नवीनतम रिलीज ZIP फ़ाइल डाउनलोड करें
3. ZIP फ़ाइल को अपनी पसंदीदा लोकेशन में एक्सट्रैक्ट करें
4. एक्सट्रैक्ट की गई फ़ोल्डर में टर्मिनल खोलें
5. स्थानीय सर्वर शुरू करें:
   ```bash
   python3 -m http.server 8000
   ```
6. अपने ब्राउज़र में `http://localhost:8000` पर जाएं

## उपयोग मार्गदर्शिका (Usage Guide)

1. **कोड लिखना (Writing Code)**
   - बाईं ओर के कोड एडिटर का उपयोग करें
   - शुरू करने के लिए ड्रॉपडाउन मेनू से उदाहरण चुनें
   - एडिटर सिंटैक्स हाइलाइटिंग और ऑटो-इंडेंटेशन का समर्थन करता है

2. **कोड चलाना (Running Code)**
   - "Run Code" बटन पर क्लिक करें या Ctrl+Enter दबाएं
   - आउटपुट दाईं पैनल में दिखाई देगा
   - आउटपुट पैनल को साफ़ करने के लिए "Clear Output" बटन का उपयोग करें

3. **उदाहरण (Examples)**
   इन बिल्ट-इन उदाहरणों को आज़माएं:
   - क्रमगुणित की गणना (Factorial Calculator)
   - फिबोनैकी श्रृंखला (Fibonacci Series)
   - सरल कैलकुलेटर (Simple Calculator)

## उदाहरण (Examples)

### क्रमगुणित की गणना (Factorial Calculator)
```
फंक्शन क्रमगुणितअ(संख्या) {
    अगर संख्या <= 1 {
        वापस 1;
    }
    वापस संख्या * क्रमगुणितअ(संख्या - 1);
}

केलिए (वैरिएबल क्रम = 1; क्रम <= 5; क्रम = क्रम + 1) {
    वैरिएबल परिणाम = क्रमगुणितअ(क्रम);
    छाप क्रम + "! = " + परिणाम;
}
```

### फिबोनैकी श्रृंखला (Fibonacci Series)
```
फंक्शन फिबोनैकी(संख्या) {
    अगर संख्या <= 1 {
        वापस संख्या;
    }
    वापस फिबोनैकी(संख्या - 1) + फिबोनैकी(संख्या - 2);
}

केलिए (वैरिएबल क्रम = 0; क्रम < 10; क्रम = क्रम + 1) {
    छाप "F(" + क्रम + ") = " + फिबोनैकी(क्रम);
}
```

### सरल कैलकुलेटर (Simple Calculator)
```
वैरिएबल पहली_संख्या = 10;
वैरिएबल दूसरी_संख्या = 5;

छाप "जोड़: " + (पहली_संख्या + दूसरी_संख्या);
छाप "घटाव: " + (पहली_संख्या - दूसरी_संख्या);
छाप "गुणा: " + (पहली_संख्या * दूसरी_संख्या);
छाप "भाग: " + (पहली_संख्या / दूसरी_संख्या);
```

## समस्या निवारण (Troubleshooting)

1. **सर्वर पहले से चल रहा है (Server Already Running)**
   यदि आप "Address already in use" त्रुटि देखते हैं:
   ```bash
   # पोर्ट 8000 का उपयोग करने वाली प्रक्रिया को खोजें
   lsof -i :8000
   # प्रक्रिया को समाप्त करें
   kill -9 <PID>
   # या पोर्ट 8000 पर चलने वाली किसी भी प्रक्रिया को समाप्त करने के लिए यह कमांड उपयोग करें
   lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
   ```

2. **ब्राउज़र समस्याएं (Browser Issues)**
   - यदि पेज ठीक से लोड नहीं होता है तो अपने ब्राउज़र का कैश साफ़ करें
   - सुनिश्चित करें कि आपके ब्राउज़र में JavaScript सक्षम है
   - आधुनिक ब्राउज़र का उपयोग करें (Chrome, Firefox, Safari, या Edge)

## तकनीकी स्टैक (Technology Stack)

- Pyiodide - ब्राउज़र में Python रनटाइम
- Ace Editor - कोड एडिटर
- Modern HTML/CSS/JavaScript
- GitHub Pages होस्टिंग के लिए

## योगदान (Contributing)

योगदान का स्वागत है! कृपया Pull Request जमा करें।

1. रिपॉजिटरी को फोर्क करें
2. अपनी फीचर ब्रांच बनाएं (`git checkout -b feature/AmazingFeature`)
3. अपने परिवर्तनों को कमिट करें (`git commit -m 'Add some AmazingFeature'`)
4. ब्रांच को पुश करें (`git push origin feature/AmazingFeature`)
5. Pull Request खोलें

## लाइसेंस (License)

यह प्रोजेक्ट MIT लाइसेंस के तहत लाइसेंस प्राप्त है - विवरण के लिए [LICENSE](LICENSE) फ़ाइल देखें।

## सहायता (Support)

यदि आपको कोई समस्या आती है या प्रश्न हैं:
1. [Issues](https://github.com/rohitm487/devnagari-lang-web/issues) पेज देखें
2. यदि आपकी समस्या पहले से रिपोर्ट नहीं की गई है तो नया इश्यू बनाएं
3. हमारी समुदाय चर्चाओं में शामिल हों
