# Jenkins Setup Guide for MLOps Salary Prediction App

This guide will help you set up Jenkins to automatically build and deploy your Docker application when changes are merged to the master branch.

## Prerequisites

1. Jenkins server with Docker support
2. Docker Hub account
3. GitHub repository with webhook support
4. Email server configuration (SMTP)

## Jenkins Configuration

### 1. Install Required Plugins

Ensure the following plugins are installed in Jenkins:
- Docker Pipeline Plugin
- Email Extension Plugin
- GitHub Plugin
- GitHub Branch Source Plugin

### 2. Configure Docker Hub Credentials

1. Go to **Jenkins Dashboard** → **Manage Jenkins** → **Manage Credentials**
2. Select **Global credentials (unrestricted)**
3. Click **Add Credentials**
4. Choose **Username with password**
5. Enter your Docker Hub credentials:
   - **Username**: Your Docker Hub username
   - **Password**: Your Docker Hub password or access token
   - **ID**: `docker-hub-credentials`
   - **Description**: Docker Hub credentials for pushing images

### 3. Configure Email Settings

1. Go to **Jenkins Dashboard** → **Manage Jenkins** → **Configure System**
2. Scroll down to **E-mail Notification** section
3. Configure SMTP settings:
   - **SMTP server**: Your email server (e.g., smtp.gmail.com)
   - **Default user e-mail suffix**: Your domain
   - **Use SMTP Authentication**: Check this
   - **User Name**: Your email address
   - **Password**: Your email password or app password
   - **Use SSL**: Check this (recommended)
   - **SMTP Port**: 587 (for TLS) or 465 (for SSL)

### 4. Update Jenkinsfile Configuration

Before running the pipeline, update these variables in the `Jenkinsfile`:

```groovy
environment {
    DOCKER_IMAGE_NAME = 'your-dockerhub-username/salary-prediction-app'  // Replace with your Docker Hub username
    EMAIL_RECIPIENTS = 'your-email@example.com'  // Replace with your email
}
```

### 5. Create Jenkins Job

1. Go to **Jenkins Dashboard** → **New Item**
2. Enter job name: `mlops-salary-prediction`
3. Select **Multibranch Pipeline**
4. Click **OK**
5. Configure the job:
   - **Branch Sources**: Add GitHub source
   - **Repository**: Your GitHub repository URL
   - **Credentials**: Add your GitHub credentials if needed
   - **Behaviors**: Add "Discover branches" and "Discover pull requests from origin"
6. Save the configuration

### 6. Configure GitHub Webhook (Optional)

To trigger builds automatically on push to master:

1. Go to your GitHub repository
2. Navigate to **Settings** → **Webhooks**
3. Click **Add webhook**
4. Enter webhook URL: `http://your-jenkins-server/github-webhook/`
5. Select **Just the push event**
6. Click **Add webhook**

## Pipeline Features

The Jenkinsfile includes:

- **Automatic triggering** on push to master branch
- **Docker image building** with version tagging
- **Docker Hub push** with both versioned and latest tags
- **Email notifications** on success and failure
- **Cleanup** of local Docker images
- **Comprehensive logging** and error handling

## Manual Build

You can also trigger builds manually:
1. Go to your Jenkins job
2. Click **Build Now**
3. Monitor the build progress in the console output

## Troubleshooting

### Common Issues

1. **Docker Hub authentication failed**
   - Verify credentials are correctly configured
   - Check if using access token instead of password

2. **Email not sending**
   - Verify SMTP configuration
   - Check firewall settings
   - Ensure email credentials are correct

3. **Build not triggering on push**
   - Verify webhook configuration
   - Check Jenkins logs for webhook events
   - Ensure repository is properly configured

4. **Docker build fails**
   - Check if Docker is running on Jenkins agent
   - Verify Dockerfile syntax
   - Check for missing dependencies

### Logs

- Build logs: Available in Jenkins job console output
- System logs: **Manage Jenkins** → **System Log**
- Email logs: Check email plugin logs

## Security Notes

- Store sensitive credentials in Jenkins credential store
- Use access tokens instead of passwords when possible
- Regularly rotate credentials
- Limit Jenkins agent permissions
- Use HTTPS for webhook URLs in production

## Next Steps

After successful setup:
1. Test the pipeline with a sample commit
2. Verify Docker image is pushed to Docker Hub
3. Check email notifications are received
4. Consider adding additional stages like testing or deployment
