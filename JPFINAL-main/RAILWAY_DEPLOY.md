# 🚂 Deploy to Railway.app - 5 Minutes Setup

## Why Railway?
- ✅ Zero configuration needed
- ✅ Auto-deploys on git push
- ✅ Free SSL for custom domains
- ✅ $5/month (500 hours free trial)
- ✅ Built-in monitoring

---

## 🚀 One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/django)

**OR follow manual steps below:**

---

## 📋 Manual Deployment Steps

### Step 1: Sign Up & Create Project
1. Go to: https://railway.app
2. Click "Login" → Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose: `ekaaiurgaa-glitch/JPFINAL`
6. Click "Deploy Now"

### Step 2: Add Environment Variables
In Railway dashboard, go to your project → Variables tab → Add these:

```env
SECRET_KEY=django-insecure-jayti-railway-prod-2026-change-this
DEBUG=False
ALLOWED_HOSTS=jaytibirthday.in,www.jaytibirthday.in,.railway.app
GEMINI_API_KEY=AIzaSyC5F5GSfJeB1_4qN5J_X8L8Tzp9KQGgGqg
TIME_ZONE=Asia/Kolkata
```

**Optional (for PostgreSQL instead of SQLite):**
```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

### Step 3: Wait for Deployment
- Railway automatically detects Django
- Builds and deploys in ~2 minutes
- You'll get a URL like: `jayti-birthday-production.up.railway.app`

### Step 4: Add Custom Domain
1. In Railway dashboard → Settings → Domains
2. Click "Add Domain"
3. Enter: `www.jaytibirthday.in`
4. Copy the CNAME record Railway provides
5. Add CNAME in your domain registrar:
   ```
   Type: CNAME
   Name: www
   Value: [Railway provides this]
   TTL: 3600
   ```
6. Wait 5-10 minutes for DNS propagation
7. Railway auto-provisions SSL certificate

### Step 5: Test Your Site
1. Visit: `https://www.jaytibirthday.in`
2. Login with: `jayati` / `jayati2026`
3. All 21 features should work! 🎉

---

## 🔄 Auto-Deploy on Git Push

Every time you push to GitHub, Railway automatically:
1. Pulls latest code
2. Installs dependencies
3. Runs migrations
4. Collects static files
5. Restarts server

**No manual deployment needed!**

---

## 📊 Monitoring & Logs

Railway dashboard shows:
- Real-time logs
- CPU/Memory usage
- Request metrics
- Deployment history

---

## 💰 Pricing

**Free Trial**: 500 hours ($5 credit)
**After Trial**: ~$5/month for this app

**Includes**:
- Unlimited deployments
- Custom domains with SSL
- 8GB RAM, 8 vCPU
- 100GB bandwidth

---

## 🆘 Troubleshooting

### Static Files Not Loading
Railway automatically runs `collectstatic` - no action needed.

### Database Not Persisting
Railway provides persistent volumes automatically for SQLite.

### Custom Domain Not Working
1. Verify CNAME record in domain registrar
2. Wait 10-30 minutes for DNS propagation
3. Check Railway logs for SSL certificate status

### App Crashes on Start
Check Railway logs:
1. Go to project → Deployments
2. Click latest deployment
3. View logs for error messages

---

## 🎯 Quick Commands

**View Logs:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# View logs
railway logs
```

**Run Migrations Manually:**
```bash
railway run python manage.py migrate
```

**Create Superuser:**
```bash
railway run python manage.py createsuperuser
```

---

## ✅ Success Checklist

- [ ] Railway project created
- [ ] GitHub repo connected
- [ ] 5 environment variables added
- [ ] First deployment successful
- [ ] Railway URL works (*.railway.app)
- [ ] Custom domain added
- [ ] CNAME record configured
- [ ] SSL certificate active
- [ ] www.jaytibirthday.in loads
- [ ] Login works (jayati/jayati2026)
- [ ] All 6 sections accessible

---

## 🎁 You're Done!

Your website is now live at:
- **https://www.jaytibirthday.in**
- **https://jaytibirthday.in** (if you add A record)

**Login**: jayati / jayati2026

All 21 features are production-ready for Jayti's birthday! 🎉

---

## 📞 Support

**Railway Docs**: https://docs.railway.app
**Railway Discord**: https://discord.gg/railway
**This Project**: https://github.com/ekaaiurgaa-glitch/JPFINAL

---

*Created with love for Jayti Pargal's birthday - February 6, 2026* ❤️
