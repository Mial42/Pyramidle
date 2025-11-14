# Deploying Pyramidle to Netlify

This guide walks you through deploying Pyramidle as a live website using Netlify.

## Prerequisites

1. **GitHub Account** - Your code is already on GitHub ✓
2. **Netlify Account** - Sign up for free at [netlify.com](https://netlify.com)
3. **Built and tested locally** - Make sure `npm run build` works

## Option 1: Deploy via Netlify UI (Recommended for First Deploy)

### Step 1: Sign Up / Log In to Netlify

1. Go to [netlify.com](https://netlify.com)
2. Click "Sign up" (or "Log in" if you have an account)
3. Choose "Sign up with GitHub" for easiest integration

### Step 2: Import Your GitHub Repository

1. Click **"Add new site"** → **"Import an existing project"**
2. Choose **"Deploy with GitHub"**
3. Authorize Netlify to access your GitHub account
4. Select the **`Pyramidle`** repository

### Step 3: Configure Build Settings

Netlify should auto-detect the settings from `netlify.toml`, but verify:

- **Base directory**: `pyramidle-app`
- **Build command**: `npm run build`
- **Publish directory**: `pyramidle-app/dist`

Click **"Deploy site"**

### Step 4: Wait for Deployment

- Netlify will install dependencies and build your app (~2-3 minutes)
- Watch the build logs if you're curious
- When complete, you'll get a URL like: `https://random-name-12345.netlify.app`

### Step 5: Test Your Site!

Visit the URL and play a round of Pyramidle to make sure everything works.

## Option 2: Deploy via Netlify CLI (For Developers)

```bash
# Install Netlify CLI globally
npm install -g netlify-cli

# Navigate to project root
cd /path/to/Pyramidle

# Login to Netlify
netlify login

# Initialize Netlify site (first time only)
netlify init

# Deploy
netlify deploy --prod
```

## Custom Domain (Optional)

### Using a Custom Domain You Own

1. Buy a domain (e.g., `pyramidle.com` from Namecheap, Google Domains, etc.)
2. In Netlify dashboard → **Domain settings** → **Add custom domain**
3. Follow Netlify's DNS instructions to point your domain to Netlify
4. Netlify provides free HTTPS/SSL automatically

### Free Netlify Subdomain

1. In site settings → **Domain management**
2. Click **"Options"** → **"Edit site name"**
3. Change from random name to something like `pyramidle.netlify.app`

## Automatic Deployments

Once connected, Netlify will automatically:
- **Deploy on push** - Every git push to your main branch triggers a new deploy
- **Preview deploys** - Pull requests get their own preview URLs
- **Rollbacks** - Easy to rollback to previous versions

## Environment Variables (If Needed Later)

If you add features requiring API keys or secrets:

1. Go to **Site settings** → **Environment variables**
2. Add variables (they'll be available during build)
3. Never commit secrets to GitHub!

## Troubleshooting

### Build Fails

**Check build logs** in Netlify dashboard for errors:
- Missing dependencies? Make sure `package.json` is correct
- Build command wrong? Verify `netlify.toml` settings
- Node version? Netlify uses Node 18 by default

### Site Loads But No Countries

Make sure the `public/data/` folder is included in your git repo:
```bash
git add pyramidle-app/public/data/
git commit -m "Ensure data files are tracked"
git push
```

### 404 Errors on Routes

The `netlify.toml` redirect rule should handle this. If not, check:
- `[[redirects]]` section exists in `netlify.toml`
- File is in the root of your repository

## Performance Tips

1. **Enable Asset Optimization** - In Build settings → Post processing
2. **Enable Brotli Compression** - Automatically enabled
3. **Use Netlify CDN** - Automatically enabled (serves from nearest location)

## Analytics (Optional)

Enable Netlify Analytics for visitor stats:
- Go to **Analytics** tab in dashboard
- Click **Enable Analytics** ($9/month)
- Or use free Google Analytics (add script to `index.html`)

## Monitoring

Check your site health:
- **Deploys tab** - See build history and logs
- **Functions tab** - If you add serverless functions later
- **Analytics** - If enabled

## Next Steps After Deployment

1. **Share the URL!** 🎉
2. **Test on mobile devices** - Make sure responsive design works
3. **Share on social media** - Get feedback from users
4. **Monitor errors** - Check Netlify logs for issues
5. **Plan features** - User accounts? Leaderboards? Backend?

## Updating the Site

Simply push to GitHub:

```bash
git add .
git commit -m "Your update message"
git push
```

Netlify auto-deploys in ~2-3 minutes!

---

**Questions?** Check [Netlify Docs](https://docs.netlify.com) or their excellent support forum.
