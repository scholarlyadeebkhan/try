// Language switching functionality for AarogyaLink - Enhanced Version
let currentLanguage = 'en';
let isLanguageDropdownOpen = false;

// Multilingual content
const translations = {
    en: {
        greeting: "Hi! I'm Dr. AarogyaLink, your AI health buddy. Tell me what's bothering you and I'll ask a few quick questions to help out. 😊\n\nRemember: For serious concerns, always see a real doctor!",
        name: "English",
        placeholder: "Tell me what's bothering you... e.g. 'Bad headache since this morning, right side, feels throbbing, also nauseous'",
        buttons: {
            send: "Send",
            record: "Start Recording",
            analyze: "Analyze Image",
            startAI: "Start AI Analysis"
        },
        // New translations for body elements
        heroTitle: "Your Personal Health Companion",
        heroSubtitle: "Connect with care, whenever you need it. Securely share your health concerns and receive expert guidance, all in one place.",
        heroCTA: "Try Now",
        howItWorksTitle: "Connect with Care, Your Way.",
        howItWorksSubtitle: "Our platform makes it simple to share your health concerns using any format you're comfortable with.",
        tryNowTitle: "Try AarogyaLink Now",
        tryNowSubtitle: "Share your health concerns in the way that works best for you",
        textTab: "Type Your Problem Here",
        uploadImage: "Upload Image",
        startWebcam: "Start Webcam",
        stopWebcam: "Stop Webcam",
        whyUsTitle: "Health is a Partnership. We're Here to Help.",
        contactTitle: "Get In Touch",
        contactSubtitle: "For all non-medical inquiries, please fill out the form below.",
        footerText: "© 2024 AarogyaLink. All rights reserved.",
        privacyPolicy: "Privacy Policy",
        termsOfService: "Terms of Service",
        getStarted: "Get Started"
    },
    hi: {
        greeting: "नमस्ते! मैं डॉ. आरोग्यलिंक हूं, आपका AI स्वास्थ्य मित्र। बताइए क्या परेशानी है, मैं कुछ सवाल पूछकर मदद करूंगा। 😊\n\nयाद रखें: गंभीर समस्याओं के लिए हमेशा असली डॉक्टर से मिलें!",
        name: "हिंदी",
        placeholder: "अपनी परेशानी बताएं... जैसे: 'सुबह से तेज सिरदर्द, दाईं तरफ, धड़कता है, जी मिचला रहा है'",
        buttons: {
            send: "भेजें",
            record: "रिकॉर्डिंग शुरू करें",
            analyze: "छवि का विश्लेषण करें",
            startAI: "AI विश्लेषण शुरू करें"
        },
        // New translations for body elements
        heroTitle: "आपका व्यक्तिगत स्वास्थ्य साथी",
        heroSubtitle: "जब भी आपको आवश्यकता हो, देखभाल के साथ कनेक्ट करें। सुरक्षित रूप से अपनी स्वास्थ्य समस्याएं साझा करें और विशेषज्ञ मार्गदर्शन प्राप्त करें, सभी एक ही स्थान पर।",
        heroCTA: "अब कोशिश करें",
        howItWorksTitle: "अपने तरीके से देखभाल के साथ कनेक्ट करें।",
        howItWorksSubtitle: "हमारा प्लेटफॉर्म आपकी स्वास्थ्य समस्याओं को साझा करना आसान बनाता है, किसी भी प्रारूप का उपयोग करके जो आपके लिए आरामदायक है।",
        tryNowTitle: "अब आरोग्यलिंक का प्रयोग करें",
        tryNowSubtitle: "अपनी स्वास्थ्य समस्याओं को उस तरीके से साझा करें जो आपके लिए सबसे अच्छा काम करता है",
        textTab: "यहां अपनी समस्या टाइप करें",
        uploadImage: "छवि अपलोड करें",
        startWebcam: "वेबकैम प्रारंभ करें",
        stopWebcam: "वेबकैम बंद करें",
        whyUsTitle: "स्वास्थ्य एक साझेदारी है। हम यहां मदद के लिए हैं।",
        contactTitle: "संपर्क में रहें",
        contactSubtitle: "सभी गैर-चिकित्सा पूछताछ के लिए, कृपया नीचे दिए गए फॉर्म को भरें।",
        footerText: "© 2024 आरोग्यलिंक। सर्वाधिकार सुरक्षित।",
        privacyPolicy: "गोपनीयता नीति",
        termsOfService: "सेवा की शर्तें",
        getStarted: "आरंभ करें"
    },
    pa: {
        greeting: "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਡਾ. ਆਰੋਗਿਆਲਿੰਕ ਹਾਂ, ਤੁਹਾਡਾ AI ਸਿਹਤ ਦੋਸਤ। ਦੱਸੋ ਕੀ ਪਰੇਸ਼ਾਨੀ ਹੈ, ਮੈਂ ਕੁਝ ਸਵਾਲ ਪੁੱਛ ਕੇ ਮਦਦ ਕਰਾਂਗਾ। 😊\n\nਯਾਦ ਰੱਖੋ: ਗੰਭੀਰ ਸਮੱਸਿਆਵਾਂ ਲਈ ਹਮੇਸ਼ਾ ਅਸਲੀ ਡਾਕਟਰ ਨੂੰ ਮਿਲੋ!",
        name: "ਪੰਜਾਬੀ",
        placeholder: "ਅਪਣੀ ਪਰੇਸ਼ਾਨੀ ਦੱਸੋ... ਜਿਵੇਂ: 'ਸਵੇਰੇ ਤੋਂ ਸਿਰ ਵਿੱਚ ਬਹੁਤ ਦਰਦ, ਸੱਜੇ ਪਾਸੇ, ਧੜਕਦਾ ਹੈ, ਜੀ ਮਿਚਲਾ ਰਿਹਾ'",
        buttons: {
            send: "ਭੇਜੋ",
            record: "ਰਿਕਾਰਡਿੰਗ ਸ਼ੁਰੂ ਕਰੋ",
            analyze: "ਤਸਵੀਰ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ",
            startAI: "AI ਵਿਸ਼ਲੇਸ਼ਣ ਸ਼ੁਰੂ ਕਰੋ"
        },
        // New translations for body elements
        heroTitle: "ਤੁਹਾਡਾ ਨਿੱਜੀ ਸਿਹਤ ਸਾਥੀ",
        heroSubtitle: "ਜਦੋਂ ਵੀ ਤੁਹਾਨੂੰ ਲੋੜ ਹੋਵੇ ਤਾਂ ਸਾਵਧਾਨੀ ਨਾਲ ਕਨੈਕਟ ਕਰੋ। ਆਪਣੀਆਂ ਸਿਹਤ ਸਮੱਸਿਆਵਾਂ ਨੂੰ ਸੁਰੱਖਿਅਤ ਢੰਗ ਨਾਲ ਸਾਂਝਾ ਕਰੋ ਅਤੇ ਮਾਹਰ ਮਾਰਗਦਰਸ਼ਨ ਪ੍ਰਾਪਤ ਕਰੋ, ਸਭ ਇੱਕੋ ਥਾਂ 'ਤੇ।",
        heroCTA: "ਹੁਣੇ ਕੋਸ਼ਿਸ਼ ਕਰੋ",
        howItWorksTitle: "ਆਪਣੇ ਢੰਗ ਨਾਲ ਸਾਵਧਾਨੀ ਨਾਲ ਕਨੈਕਟ ਕਰੋ।",
        howItWorksSubtitle: "ਸਾਡਾ ਪਲੇਟਫਾਰਮ ਤੁਹਾਡੀਆਂ ਸਿਹਤ ਸਮੱਸਿਆਵਾਂ ਨੂੰ ਸਾਂਝਾ ਕਰਨਾ ਸੌਖਾ ਬਣਾਉਂਦਾ ਹੈ, ਕਿਸੇ ਵੀ ਫਾਰਮੈਟ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਜੋ ਤੁਹਾਨੂੰ ਆਰਾਮਦਾਇਕ ਲੱਗਦਾ ਹੈ।",
        tryNowTitle: "ਹੁਣ AarogyaLink ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰੋ",
        tryNowSubtitle: "ਆਪਣੀਆਂ ਸਿਹਤ ਸਮੱਸਿਆਵਾਂ ਨੂੰ ਉਸ ਢੰਗ ਨਾਲ ਸਾਂਝਾ ਕਰੋ ਜੋ ਤੁਹਾਨੂੰ ਸਭ ਤੋਂ ਵਧੀਆ ਲੱਗਦਾ ਹੈ",
        textTab: "ਇੱਥੇ ਆਪਣੀ ਸਮੱਸਿਆ ਟਾਈਪ ਕਰੋ",
        uploadImage: "ਚਿੱਤਰ ਅਪਲੋਡ ਕਰੋ",
        startWebcam: "ਵੈੱਬਕੈਮ ਸ਼ੁਰੂ ਕਰੋ",
        stopWebcam: "ਵੈੱਬਕੈਮ ਬੰਦ ਕਰੋ",
        whyUsTitle: "ਸਿਹਤ ਇੱਕ ਭਾਈਵਾਲਾ ਹੈ। ਅਸੀਂ ਮਦਦ ਲਈ ਇੱਥੇ ਹਾਂ।",
        contactTitle: "ਸੰਪਰਕ ਵਿੱਚ ਰਹੋ",
        contactSubtitle: "ਸਾਰੀਆਂ ਗੈਰ-ਮੈਡੀਕਲ ਪੁੱਛਗਿੱਛਾਂ ਲਈ, ਕਿਰਪਾ ਕਰਕੇ ਹੇਠਾਂ ਦਿੱਤਾ ਫਾਰਮ ਭਰੋ।",
        footerText: "© 2024 ਆਰੋਗਿਆਲਿੰਕ। ਸਾਰੇ ਹੱਕ ਰਾਖਵੇਂ ਹਨ।",
        privacyPolicy: "ਪਰਾਈਵੇਸੀ ਨੀਤੀ",
        termsOfService: "ਸੇਵਾ ਦੀਆਂ ਸ਼ਰਤਾਂ",
        getStarted: "ਸ਼ੁਰੂ ਕਰੋ"
    },
    or: {
        greeting: "ନମସ୍କାର! ମୁଁ ଡଃ ଅରୋଗ୍ୟଲିଙ୍କ, ଆପଣଙ୍କର AI ସ୍ୱାସ୍ଥ୍ୟ ସାଙ୍ଗ। ମୋତେ କୁହନ୍ତୁ କ’ଣ ଆପଣଙ୍କୁ ବ୍ୟାହାତ କରୁଛି ଏବଂ ମୁଁ କିଛି ତୁରନ୍ତ ପ୍ରଶ୍ନ ପଚାରି ସାହାଯ୍ୟ କରିବି। 😊\n\nମନେରଖନ୍ତୁ: ଗୁରୁତର ଚିନ୍ତା, ସର୍ବଦା ଏକ ବାସ୍ତବ ଡାକ୍ତରଙ୍କୁ ଦେଖନ୍ତୁ!",
        name: "ଓଡ଼ିଆ",
        placeholder: "ମୋତେ କୁହନ୍ତୁ କ’ଣ ଆପଣଙ୍କୁ ବ୍ୟାହାତ କରୁଛି... ଉଦାହରଣ: 'କାଲିଠାରୁ କଡ଼ା ମୁଖର ବ୍ୟାଥା, ଡାହାଣ ପାର୍ଶ୍ୱ, ଧକଧକି ଅନୁଭବ ହୁଏ, ମଧ୍ୟ ବାନ୍ତି ଲାଗୁଛି'",
        buttons: {
            send: "ପଠାନ୍ତୁ",
            record: "ରେକର୍ଡିଂ ଆରମ୍ଭ କରନ୍ତୁ",
            analyze: "ଛବିର ବିଶ୍ଳେଷଣ କରନ୍ତୁ",
            startAI: "AI ବିଶ୍ଳେଷଣ ଆରମ୍ଭ କରନ୍ତୁ"
        },
        // New translations for body elements
        heroTitle: "ଆପଣଙ୍କର ବ୍ୟକ୍ତିଗତ ସ୍ୱାସ୍ଥ୍ୟ ସାଙ୍ଗ",
        heroSubtitle: "ଯେତେବେଲେ ଆପଣଙ୍କୁ ଆବଶ୍ୟକତା ହୁଏ, ସାବଧାନତା ସହିତ ସଂଯୋଗ କରନ୍ତୁ। ନିରାପଦରେ ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ ଚିନ୍ତାଗୁଡିକ ସେୟାର୍ କରନ୍ତୁ ଏବଂ ବିଶେଷଜ୍ଞ ମାର୍ଗଦର୍ଶନ ପାଆନ୍ତୁ, ସବୁ ଗୋଟିଏ ସ୍ଥାନରେ।",
        heroCTA: "ବର୍ତ୍ତମାନ ଚେଷ୍ଟା କରନ୍ତୁ",
        howItWorksTitle: "ଆପଣଙ୍କ ପଦ୍ଧତିରେ ସାବଧାନତା ସହିତ ସଂଯୋଗ କରନ୍ତୁ।",
        howItWorksSubtitle: "ଆମ ପ୍ଲାଟଫର୍ମ ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ ଚିନ୍ତାଗୁଡିକୁ ସେୟାର୍ କରିବା ସରଳ କରିଥାଏ, ଯେକୌଣସି ଫର୍ମାଟ୍ ବ୍ୟବହାର କରି ଯାହା ଆପଣଙ୍କ ପାଇଁ ସୁବିଧାଜନକ।",
        tryNowTitle: "ବର୍ତ୍ତମାନ ଅରୋଗ୍ୟଲିଙ୍କ୍ ଚେଷ୍ଟା କରନ୍ତୁ",
        tryNowSubtitle: "ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ ଚିନ୍ତାଗୁଡିକୁ ସେହି ପଦ୍ଧତିରେ ସେୟାର୍ କରନ୍ତୁ ଯାହା ଆପଣଙ୍କ ପାଇଁ ସବୁଠାରେ ଭଲ କାମ କରିଥାଏ",
        textTab: "ଏଠାରେ ଆପଣଙ୍କର ସମସ୍ୟା ଟାଇପ୍ କରନ୍ତୁ",
        uploadImage: "ଛବି ଅପଲୋଡ୍ କରନ୍ତୁ",
        startWebcam: "ୱେବକ୍ୟାମ୍ ଆରମ୍ଭ କରନ୍ତୁ",
        stopWebcam: "ୱେବକ୍ୟାମ୍ ବନ୍ଦ କରନ୍ତୁ",
        whyUsTitle: "ସ୍ୱାସ୍ଥ୍ୟ ଏକ ସାଝେଦାରୀ। ଆମେ ସାହାଯ୍ୟ ପାଇଁ ଏଠାରେ ଅଛୁ।",
        contactTitle: "ସମ୍ପର୍କରେ ରହନ୍ତୁ",
        contactSubtitle: "ସମସ୍ତ ଅ-ଚିକିତ୍ସା ପ୍ରଶ୍ନଗୁଡିକ ପାଇଁ, ଦୟାକରି ନିମ୍ନଲିଖିତ ଫର୍ମଟି ପୂରଣ କରନ୍ତୁ।",
        footerText: "© 2024 ଅରୋଗ୍ୟଲିଙ୍କ୍। ସମସ୍ତ ଅଧିକାର ସୁରକ୍ଷିତ।",
        privacyPolicy: "ଗୋପନୀୟତା ନୀତି",
        termsOfService: "ସେବାର ସର୍ତ୍ତାବଳୀ",
        getStarted: "ଆରମ୍ଭ କରନ୍ତୁ"
    }
};

function toggleLanguageDropdown() {
    const dropdown = document.getElementById('languageDropdown');
    
    if (!dropdown) {
        console.warn('Language dropdown element not found');
        return;
    }
    
    isLanguageDropdownOpen = !isLanguageDropdownOpen;
    
    if (isLanguageDropdownOpen) {
        dropdown.classList.add('show');
    } else {
        dropdown.classList.remove('show');
    }
}

function changeLanguage(langCode) {
    if (!translations[langCode]) {
        console.error('Invalid language code:', langCode);
        return;
    }
    
    currentLanguage = langCode;
    const currentLangElement = document.getElementById('currentLanguage');
    
    // Update language display
    if (currentLangElement) {
        currentLangElement.textContent = translations[langCode].name;
    }
    
    // Update active language option
    document.querySelectorAll('.language-option').forEach(option => {
        option.classList.remove('active');
    });
    
    const activeOption = document.querySelector(`[data-lang="${langCode}"]`);
    if (activeOption) {
        activeOption.classList.add('active');
    }
    
    // Close dropdown
    if (isLanguageDropdownOpen) {
        toggleLanguageDropdown();
    }
    
    // Update UI elements
    updateLanguageContent(langCode);
    
    // Save language preference
    localStorage.setItem('preferredLanguage', langCode);
    
    // Update greeting message
    updateGreetingMessage(langCode);
    
    console.log('Language changed to:', translations[langCode].name);
}

function updateLanguageContent(langCode) {
    const lang = translations[langCode];
    
    if (!lang) {
        console.error('Language not found:', langCode);
        return;
    }
    
    // Update hero section
    const heroTitle = document.querySelector('#hero h1');
    if (heroTitle) heroTitle.textContent = lang.heroTitle;
    
    const heroSubtitle = document.querySelector('#hero p');
    if (heroSubtitle) heroSubtitle.textContent = lang.heroSubtitle;
    
    const heroCTA = document.querySelector('#hero a');
    if (heroCTA) heroCTA.textContent = lang.heroCTA;
    
    // Update how it works section
    const howItWorksTitle = document.querySelector('#how-it-works h2');
    if (howItWorksTitle) howItWorksTitle.textContent = lang.howItWorksTitle;
    
    const howItWorksSubtitle = document.querySelector('#how-it-works p');
    if (howItWorksSubtitle) howItWorksSubtitle.textContent = lang.howItWorksSubtitle;
    
    // Update try now section
    const tryNowTitle = document.querySelector('#chat h2');
    if (tryNowTitle) tryNowTitle.textContent = lang.tryNowTitle;
    
    const tryNowSubtitle = document.querySelector('#chat .text-center p');
    if (tryNowSubtitle) tryNowSubtitle.textContent = lang.tryNowSubtitle;
    
    // Update tab labels
    const textTab = document.querySelector('[onclick="switchTab(\'type\')"]');
    if (textTab) textTab.innerHTML = `<span class="material-symbols-outlined tab-icon">edit</span> ${lang.textTab}`;
    
    // Update why us section
    const whyUsTitle = document.querySelector('#why-us h2');
    if (whyUsTitle) whyUsTitle.textContent = lang.whyUsTitle;
    
    // Update contact section
    const contactTitle = document.querySelector('#contact h2');
    if (contactTitle) contactTitle.textContent = lang.contactTitle;
    
    const contactSubtitle = document.querySelector('#contact p');
    if (contactSubtitle) contactSubtitle.textContent = lang.contactSubtitle;
    
    // Update footer
    const footerText = document.querySelector('footer p');
    if (footerText) footerText.textContent = lang.footerText;
    
    const privacyPolicy = document.querySelector('footer a:first-child');
    if (privacyPolicy) privacyPolicy.textContent = lang.privacyPolicy;
    
    const termsOfService = document.querySelector('footer a:last-child');
    if (termsOfService) termsOfService.textContent = lang.termsOfService;
    
    // Update floating CTA
    const floatingCTA = document.querySelector('#floatingCTA span:last-child');
    if (floatingCTA) floatingCTA.textContent = lang.getStarted;
    
    // Update text input placeholder
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.placeholder = lang.placeholder;
    }
    
    // Update button texts
    const sendButton = document.querySelector('button[onclick="sendTextMessage()"] .material-symbols-outlined');
    if (sendButton && lang.buttons.send) {
        sendButton.setAttribute('title', lang.buttons.send);
    }
    
    const recordButton = document.getElementById('recordButton');
    if (recordButton && lang.buttons.record) {
        recordButton.textContent = lang.buttons.record;
    }
}

function updateGreetingMessage(langCode) {
    const chatContainer = document.getElementById('chatContainer');
    if (!chatContainer) return;
    
    const existingGreeting = chatContainer.querySelector('.message.ai .message-bubble');
    
    if (existingGreeting && translations[langCode]) {
        existingGreeting.innerHTML = formatMessageContent(translations[langCode].greeting);
        
        // Add a subtle animation to indicate language change
        existingGreeting.style.transform = 'scale(0.95)';
        existingGreeting.style.opacity = '0.8';
        
        setTimeout(() => {
            existingGreeting.style.transform = 'scale(1)';
            existingGreeting.style.opacity = '1';
        }, 200);
    }
}

function formatMessageContent(content) {
    // Convert newlines to HTML breaks
    return content.replace(/\n/g, '<br>');
}

function initializeLanguage() {
    // Load saved language preference
    const savedLanguage = localStorage.getItem('preferredLanguage') || 'en';
    
    if (savedLanguage !== 'en') {
        changeLanguage(savedLanguage);
    }
    
    // Set up event listeners
    setupLanguageEventListeners();
}

function setupLanguageEventListeners() {
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const languageSwitcher = event.target.closest('.language-switcher');
        
        if (!languageSwitcher && isLanguageDropdownOpen) {
            toggleLanguageDropdown();
        }
    });
    
    // Prevent dropdown from closing when clicking inside
    const dropdown = document.getElementById('languageDropdown');
    if (dropdown) {
        dropdown.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing language system...');
    initializeLanguage();
});

// Export functions for global access
window.toggleLanguageDropdown = toggleLanguageDropdown;
window.changeLanguage = changeLanguage;
window.currentLanguage = () => currentLanguage;