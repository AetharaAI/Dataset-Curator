# BlackBox Audio - Landing Page

> Private unlimited AI voice cloning and music generation. Built by a master electrician and musician. US sovereign infrastructure.

## 🚀 Quick Start

This is a production-ready, single-page landing page for BlackBox Audio. Zero framework dependencies, optimized for performance, and ready to deploy.

### Files Structure

```
BlackBox-Audio/
├── index.html              # Main landing page (includes inline critical CSS)
├── assets/
│   ├── styles.css          # Non-critical deferred styles
│   └── main.js             # All JavaScript functionality
├── public/
│   ├── blackbox-logo.png
│   ├── blackbox-audio-stack-logo.png
│   └── blackbox-audio-3d-cube-logoZ.png
└── README.md               # This file
```

### Tech Stack

- **HTML5** - Semantic, accessible, SEO-optimized
- **Pure CSS3** - CSS Custom Properties, no preprocessors
- **Vanilla JavaScript ES6+** - No jQuery, no React, no frameworks
- **Performance** - Critical CSS inlined, lazy-loaded images, optimized for Core Web Vitals
- **Accessibility** - WCAG AA compliant, keyboard navigation, screen reader friendly

## 📦 Deployment Options

### Option 1: Cloudflare Pages (Recommended - Free)

1. **Sign up for Cloudflare Pages** (if you haven't already)
   - Go to https://pages.cloudflare.com

2. **Connect your Git repository**
   - Click "Create a project"
   - Connect to your GitHub account
   - Select this repository

3. **Configure build settings**
   - Build command: (leave empty - static site)
   - Build output directory: `/`
   - Root directory: `/`

4. **Deploy**
   - Click "Save and Deploy"
   - Your site will be live at `https://your-project.pages.dev`

5. **Add custom domain**
   - Go to your project settings
   - Add your custom domain (e.g., `blackboxaudio.com`)
   - Follow DNS configuration instructions

**Cloudflare Pages Features:**
- ✅ Free SSL/TLS certificate
- ✅ Global CDN
- ✅ Automatic deployments on git push
- ✅ Preview deployments for branches
- ✅ Web Analytics (optional)

### Option 2: Netlify (Free)

1. **Sign up for Netlify**
   - Go to https://www.netlify.com

2. **New site from Git**
   - Click "Add new site" → "Import an existing project"
   - Connect to your Git provider (GitHub)
   - Select this repository

3. **Configure build settings**
   - Build command: (leave empty)
   - Publish directory: `/`

4. **Deploy**
   - Click "Deploy site"
   - Your site will be live at `https://random-name.netlify.app`

5. **Add custom domain**
   - Go to "Domain settings"
   - Add custom domain
   - Configure DNS

**Netlify Features:**
- ✅ Free SSL/TLS certificate
- ✅ CDN
- ✅ Continuous deployment
- ✅ Form handling (can use for waitlist)
- ✅ Edge functions (optional)

### Option 3: Vercel (Free)

1. **Sign up for Vercel**
   - Go to https://vercel.com

2. **Import Git repository**
   - Click "New Project"
   - Import from GitHub
   - Select this repository

3. **Configure project**
   - Framework Preset: Other
   - Build command: (leave empty)
   - Output directory: `./`

4. **Deploy**
   - Click "Deploy"
   - Live at `https://your-project.vercel.app`

5. **Add custom domain**
   - Go to project settings → Domains
   - Add your domain

### Option 4: Traditional Web Host (cPanel/FTP)

1. **Upload files via FTP**
   ```
   - Upload all files to public_html/ or www/
   - Maintain directory structure
   ```

2. **Configure HTTPS**
   - Use Let's Encrypt (usually available in cPanel)
   - Enable SSL/TLS certificate for your domain

3. **Enable Gzip/Brotli compression**
   - Add to .htaccess:
   ```apache
   <IfModule mod_deflate.c>
     AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
   </IfModule>
   ```

## ⚙️ Configuration

### 1. Stripe Integration

**IMPORTANT:** Update Stripe configuration before going live.

Edit `/assets/main.js`:

```javascript
const STRIPE_CONFIG = {
    priceTiers: {
        voice: 'price_XXXXXXXXXXXXX',      // Your Voice tier price ID
        studio: 'price_XXXXXXXXXXXXX',     // Your Studio tier price ID
        sovereign: 'price_XXXXXXXXXXXXX'   // Your Sovereign tier price ID
    },
    testMode: false,  // Set to false for production
    checkoutBaseUrl: 'https://checkout.stripe.com/pay'
};
```

**How to get Stripe Price IDs:**

1. Log in to Stripe Dashboard (https://dashboard.stripe.com)
2. Go to Products
3. Create three products:
   - **Voice Tier** - $799/month recurring
   - **Studio Tier** - $1,499/month recurring
   - **Sovereign Tier** - $3,999/month recurring
4. Copy the Price IDs (starts with `price_`)
5. Replace the test IDs in `main.js`

**Stripe Checkout Implementation Options:**

**Option A: Direct Checkout Links (No Backend Required)**
- Simplest option
- Users click button → redirected to Stripe Checkout
- Uncomment the "Option 1" code in `handleCheckout()` function

**Option B: Backend Checkout Session (Recommended for Production)**
- More control over checkout flow
- Can add metadata, customer details, etc.
- Requires a backend endpoint (Node.js, Python, PHP, etc.)
- See Stripe docs: https://stripe.com/docs/checkout/quickstart

### 2. Waitlist Integration

Edit `/assets/main.js` in the `handleWaitlist()` function:

**Option A: Use a Form Service (Easiest)**
- [Mailchimp](https://mailchimp.com)
- [ConvertKit](https://convertkit.com)
- [Buttondown](https://buttondown.email)
- Simply POST the email to their API endpoint

**Option B: Use Netlify Forms (if hosting on Netlify)**
```html
<!-- In index.html, add to form tag: -->
<form class="email-form" name="waitlist" method="POST" data-netlify="true">
    <input type="hidden" name="form-name" value="waitlist">
    <!-- rest of form -->
</form>
```

**Option C: Your Own Backend**
- Create an endpoint (e.g., `/api/waitlist`)
- Store emails in database
- Send confirmation emails
- Uncomment "Option 2" code in `handleWaitlist()` function

### 3. Analytics Integration

**Google Analytics 4:**

Add to `<head>` in `index.html`:

```html
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Plausible Analytics (Privacy-friendly alternative):**

```html
<script defer data-domain="blackboxaudio.com" src="https://plausible.io/js/script.js"></script>
```

**Cloudflare Web Analytics (Free):**

```html
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "your-token"}'></script>
```

### 4. Color Theme Customization

All colors are defined in CSS Custom Properties in `index.html` (inline styles):

```css
:root {
    /* Base Purple Backgrounds */
    --bg-primary: #0a0614;
    --bg-secondary: #150a1f;
    --bg-tertiary: #1f0f2e;

    /* Orange Spectrum */
    --orange-bright: #ff6b35;
    --orange-mid: #ff8c42;
    --orange-light: #ffa552;
    --orange-dark: #cc4e1f;

    /* Change any of these values to customize the theme */
}
```

### 5. Content Customization

**Update Text Content:**
- Edit `index.html` directly
- All content is in semantic HTML sections
- Search for specific text to replace

**Update Images:**
- Replace files in `/public/` directory
- Keep the same filenames, or update paths in `index.html`

**Update Pricing:**
- Edit the pricing cards in the `<section class="pricing">` section
- Update prices, features, and CTA text

## 🔧 Development

### Local Development Server

**Option 1: Using Python (if installed):**
```bash
# Python 3
python -m http.server 8000

# Then open: http://localhost:8000
```

**Option 2: Using Node.js:**
```bash
npx serve .

# Then open: http://localhost:3000
```

**Option 3: Using PHP:**
```bash
php -S localhost:8000
```

**Option 4: VS Code Live Server Extension**
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

### Performance Testing

**Test Core Web Vitals:**
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [GTmetrix](https://gtmetrix.com/)
- [WebPageTest](https://www.webpagetest.org/)

**Target Metrics:**
- ✅ LCP (Largest Contentful Paint): < 2.5s
- ✅ FID (First Input Delay): < 100ms
- ✅ CLS (Cumulative Layout Shift): < 0.1

### Accessibility Testing

- [WAVE Browser Extension](https://wave.webaim.org/extension/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- Lighthouse Accessibility Audit (Chrome DevTools)

**Keyboard Navigation Test:**
1. Tab through all interactive elements
2. Ensure focus states are visible
3. Test FAQ accordions with Enter/Space keys
4. Test mobile menu toggle

## 🔒 Security

### Content Security Policy (Recommended)

Add to your hosting provider's headers or use a `<meta>` tag:

```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'unsafe-inline' https://checkout.stripe.com https://js.stripe.com;
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    font-src 'self' https://fonts.gstatic.com;
    img-src 'self' data: https:;
    connect-src 'self' https://checkout.stripe.com;
">
```

### HTTPS Only

- Always use HTTPS in production
- All deployment options above provide free SSL/TLS
- Never collect payment info without HTTPS

## 📱 Browser Support

- ✅ Chrome/Edge (last 2 versions)
- ✅ Firefox (last 2 versions)
- ✅ Safari (last 2 versions)
- ✅ Mobile Safari (iOS 12+)
- ✅ Chrome Mobile (Android 8+)

**Fallbacks included for:**
- CSS Grid → Flexbox
- CSS Custom Properties → Inline values
- Intersection Observer → Immediate visibility
- Backdrop filter → Solid background

## 🐛 Troubleshooting

### Images not loading
- Check file paths are correct
- Ensure `/public/` directory is accessible
- Verify image files are uploaded

### Stripe checkout not working
- Verify Price IDs are correct in `main.js`
- Check browser console for errors
- Ensure checkboxes are checked before clicking button
- Test in Stripe test mode first

### Animations not playing
- Check if user has `prefers-reduced-motion` enabled
- Verify JavaScript is enabled
- Check browser console for errors

### Mobile menu not working
- Ensure JavaScript loaded correctly
- Check for console errors
- Verify event listeners are attached

## 📊 SEO Optimization

### Pre-Launch Checklist

- ✅ Update `<title>` with your domain/keywords
- ✅ Update meta descriptions
- ✅ Add favicon (already set to logo)
- ✅ Create `sitemap.xml` (for multi-page sites)
- ✅ Create `robots.txt` (if needed)
- ✅ Set up Google Search Console
- ✅ Submit sitemap to Google
- ✅ Set up Open Graph images
- ✅ Test with [Facebook Debugger](https://developers.facebook.com/tools/debug/)
- ✅ Test with [Twitter Card Validator](https://cards-dev.twitter.com/validator)

### robots.txt (Optional)

Create `/robots.txt`:
```
User-agent: *
Allow: /
Sitemap: https://blackboxaudio.com/sitemap.xml
```

### sitemap.xml (Optional for single page)

Create `/sitemap.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://blackboxaudio.com/</loc>
    <lastmod>2025-11-21</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

## 🎨 Design System Reference

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Background | `#0a0614` | Main background |
| Secondary Background | `#150a1f` | Cards, elevated surfaces |
| Tertiary Background | `#1f0f2e` | Section breaks |
| Orange Bright | `#ff6b35` | Primary CTA, accents |
| Orange Mid | `#ff8c42` | Gradients |
| Orange Light | `#ffa552` | Highlights |
| Purple Glow | `#8b5cf6` | Interactive states |
| Text Primary | `#f5f0ff` | Headings, important text |
| Text Secondary | `#b8a8cc` | Body text, descriptions |

### Typography

- **Headlines:** Space Grotesk (600-700 weight)
- **Body:** Inter (400-500 weight)
- **Base Size:** 16px
- **Scale:** 18px body, 24-72px headlines

### Spacing

- **Section Padding:** 120px vertical, 24px horizontal
- **Container Max Width:** 1200px
- **Grid Gap:** 32-48px

## 📝 License & Credits

### Project License
This landing page was built for BlackBox Audio by AetherPro Technologies LLC.

### Open Source Dependencies
- [Google Fonts](https://fonts.google.com/) - Space Grotesk, Inter
- No other external dependencies - 100% vanilla code

### Image Assets
- Logo and branding images © BlackBox Audio / AetherPro Technologies LLC

## 🚀 Going Live Checklist

Before you deploy to production:

- [ ] Update all Stripe Price IDs in `main.js`
- [ ] Set `testMode: false` in Stripe config
- [ ] Configure waitlist form backend/service
- [ ] Add analytics tracking code
- [ ] Test all form submissions
- [ ] Test all pricing tier checkouts
- [ ] Test on mobile devices
- [ ] Run Lighthouse audit
- [ ] Test accessibility with screen reader
- [ ] Verify all links work
- [ ] Check for console errors
- [ ] Optimize images (already optimized)
- [ ] Set up custom domain DNS
- [ ] Enable SSL/TLS certificate
- [ ] Configure email for contact forms
- [ ] Test page speed
- [ ] Submit to search engines
- [ ] Set up monitoring/uptime alerts

## 📞 Support

For questions about this landing page:
- Review the code comments
- Check browser console for errors
- Verify all configuration steps above

For Stripe questions:
- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Support](https://support.stripe.com/)

---

**Built by Cory Gibson - Licensed Master Electrician & Musician - Midwest Sovereign Iron**

**BlackBox Audio** - Private unlimited AI voice cloning and music generation. US soil. Zero compromises.
