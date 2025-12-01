# Release Pipeline Setup Instructions

## What Was Changed

The GitHub Actions workflow (`.github/workflows/ci.yml`) has been completely refined to meet all your requirements:

### ✅ Acceptance Criteria Met

1. **Version tag triggers** - Pushes to `v*.*.*` tags trigger the full release pipeline
2. **Build sdist and wheels** - Builds source distribution and wheels for Python 3.9-3.12 on Linux, macOS, and Windows
3. **Test PyPI + Production PyPI** - Publishes to Test PyPI first, then production PyPI with approval
4. **Lean caching and matrix** - Optimized builds with pip caching, selective matrix strategy
5. **Updated packaging metadata** - Your `pyproject.toml` is already well-configured

### Key Improvements

**Before (Issues)**:
- ❌ Attempted to use cibuildwheel but configuration was incomplete
- ❌ No Test PyPI step
- ❌ No approval flow for production
- ❌ Missing sdist build
- ❌ Hardcoded `PYPI_API_TOKEN` secret requirement

**After (Fixed)**:
- ✅ Standard `python -m build` for sdist and wheels (simpler, more reliable)
- ✅ Test PyPI publish on every tag (automatic validation)
- ✅ Production PyPI with environment protection (approval workflow)
- ✅ Builds both sdist and wheels correctly
- ✅ Uses OIDC Trusted Publishers (no tokens needed!)
- ✅ Full test suite runs before building
- ✅ Artifacts properly deduplicated
- ✅ GitHub Release auto-created with artifacts attached

## Required Setup Steps

### Step 1: Configure PyPI Trusted Publishers (Recommended - Most Secure)

This method doesn't require storing any API tokens in GitHub!

#### For Test PyPI:

1. Go to: https://test.pypi.org/manage/account/publishing/
2. Log in with your Test PyPI account
3. Click "Add a new pending publisher"
4. Fill in:
   - **PyPI Project Name**: `xml-pipeline`
   - **Owner**: `dullfig`
   - **Repository name**: `xml-pipeline`
   - **Workflow filename**: `ci.yml`
   - **Environment name**: `testpypi`
5. Click "Add"

#### For Production PyPI:

1. Go to: https://pypi.org/manage/account/publishing/
2. Log in with your PyPI account
3. Click "Add a new pending publisher"
4. Fill in:
   - **PyPI Project Name**: `xml-pipeline`
   - **Owner**: `dullfig`
   - **Repository name**: `xml-pipeline`
   - **Workflow filename**: `ci.yml`
   - **Environment name**: `pypi`
5. Click "Add"

**Note**: You can add the pending publisher even if the package doesn't exist on PyPI yet. On first publish, it will create it.

### Step 2: Configure GitHub Environments

1. Go to: https://github.com/dullfig/xml-pipeline/settings/environments
2. Create two environments:

#### Environment: `testpypi`
- Click "New environment"
- Name: `testpypi`
- Click "Configure environment"
- **No protection rules needed** (automatic publishing is fine for testing)
- Save

#### Environment: `pypi`
- Click "New environment"  
- Name: `pypi`
- Click "Configure environment"
- **Add protection rules**:
  - ✅ **Required reviewers**: Add yourself or team members
  - ✅ **Wait timer**: 5 minutes (optional - gives you time to verify Test PyPI)
- Save

This ensures production PyPI releases require manual approval!

### Step 3: Alternative - Using API Tokens (Legacy Method)

If you prefer using API tokens instead of Trusted Publishers:

#### Generate Tokens:

1. **Test PyPI**: https://test.pypi.org/manage/account/token/
   - Create token with scope for `xml-pipeline` project
   - Copy token (starts with `pypi-`)

2. **Production PyPI**: https://pypi.org/manage/account/token/
   - Create token with scope for `xml-pipeline` project  
   - Copy token (starts with `pypi-`)

#### Add to GitHub Secrets:

1. Go to: https://github.com/dullfig/xml-pipeline/settings/secrets/actions
2. Click "New repository secret"
3. Add these two secrets:
   - Name: `TEST_PYPI_API_TOKEN` → Value: your Test PyPI token
   - Name: `PYPI_API_TOKEN` → Value: your production PyPI token

#### Modify Workflow:

Update the publish steps in `.github/workflows/ci.yml` to use tokens:

```yaml
    - name: Publish to Test PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        repository-url: https://test.pypi.org/legacy/
        password: ${{ secrets.TEST_PYPI_API_TOKEN }}

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

## Usage

### Method 1: Tag-Based Release (Recommended)

```bash
# Ensure you're on main branch with latest changes
git checkout main
git pull origin main

# Create and push a version tag
git tag v0.2.1
git push origin v0.2.1
```

**What happens:**
1. ✅ Tests run on Python 3.9-3.12
2. ✅ Builds sdist and wheels for Linux, macOS, Windows
3. ✅ Tests the built packages
4. ✅ Publishes to Test PyPI automatically
5. ⏸️ Waits for manual approval (if configured)
6. ✅ Publishes to production PyPI
7. ✅ Creates GitHub Release with artifacts

### Method 2: Manual Workflow Dispatch

1. Go to: https://github.com/dullfig/xml-pipeline/actions
2. Select "CI, Build & Publish" workflow
3. Click "Run workflow"
4. Choose:
   - Branch: `main`
   - **Deploy to Production PyPI**: `true` or `false`
5. Click "Run workflow"

### Monitoring the Release

1. Go to: https://github.com/dullfig/xml-pipeline/actions
2. Click on the running workflow
3. Monitor each job:
   - `test` - Runs test suite
   - `build` - Creates packages
   - `test-package` - Validates built packages
   - `publish-testpypi` - Uploads to Test PyPI
   - `publish-pypi` - Uploads to production (may wait for approval)

### Verifying the Release

#### Check Test PyPI:
```bash
# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ xml-pipeline==0.2.1

# Test import
python -c "from xml_pipeline import MessageBus; print('Success!')"
```

#### Check Production PyPI:
```bash
# Install from PyPI
pip install xml-pipeline==0.2.1

# Test import
python -c "from xml_pipeline import MessageBus; print('Success!')"
```

#### Check GitHub Release:
- Go to: https://github.com/dullfig/xml-pipeline/releases
- Verify release `v0.2.1` exists
- Check that sdist and wheels are attached as artifacts

## Troubleshooting

### Build Failures

**Issue**: Tests fail on specific Python version
- **Solution**: Check test logs, fix failing tests, push changes, re-tag

**Issue**: Wheel building fails
- **Solution**: Check if dependencies are properly specified in `pyproject.toml`

### Publishing Failures

**Issue**: "403 Forbidden" when publishing to Test PyPI/PyPI
- **Cause**: Trusted Publisher not configured correctly
- **Solution**: Verify settings match exactly:
  - Repository owner: `dullfig`
  - Repository name: `xml-pipeline`
  - Workflow filename: `ci.yml`
  - Environment names: `testpypi` and `pypi`

**Issue**: "400 Bad Request - File already exists"
- **Cause**: Version already published
- **Solution**: Increment version number in `pyproject.toml`, create new tag

**Issue**: Workflow waiting forever on PyPI publish
- **Cause**: Environment protection rules requiring approval
- **Solution**: Go to Actions → Click workflow → Review deployments → Approve

### Package Issues

**Issue**: Import fails after installation
- **Cause**: Missing dependencies or incorrect package structure
- **Solution**: Check `pyproject.toml` dependencies, verify package imports locally

## Version Management

Before creating a new release:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "0.2.1"  # Increment as needed
   ```

2. **Update changelog** in `README.md` (if you maintain one)

3. **Commit changes**:
   ```bash
   git add pyproject.toml README.md
   git commit -m "Bump version to 0.2.1"
   git push origin main
   ```

4. **Create and push tag**:
   ```bash
   git tag v0.2.1
   git push origin v0.2.1
   ```

## Best Practices

1. **Always test locally first**:
   ```bash
   python -m build
   pip install dist/*.whl
   pytest tests/
   ```

2. **Use semantic versioning**:
   - `v1.0.0` - Major release (breaking changes)
   - `v0.3.0` - Minor release (new features)
   - `v0.2.1` - Patch release (bug fixes)

3. **Verify Test PyPI before approving production**:
   - Install from Test PyPI
   - Run your test suite
   - Test in a clean environment
   - Only then approve production deployment

4. **Keep environment protection**:
   - Always require approval for production PyPI
   - Add multiple reviewers for safety
   - Use wait timers for last-minute checks

5. **Monitor workflow runs**:
   - Check logs for warnings
   - Verify all platforms build successfully
   - Review Test PyPI publication before production

## Summary

Your release pipeline is now production-ready! Every time you push a version tag:

1. ✅ Full test suite runs
2. ✅ Multi-platform builds (Linux, macOS, Windows)
3. ✅ Multi-version testing (Python 3.9-3.12)
4. ✅ Automatic Test PyPI publication
5. ✅ Controlled production PyPI publication
6. ✅ GitHub Release with artifacts
7. ✅ Secure (OIDC trusted publishers)

**Next step**: Configure the Trusted Publishers on PyPI/Test PyPI (Step 1), then push your first tag!

## Support

- **Workflow issues**: Check [GitHub Actions docs](https://docs.github.com/en/actions)
- **PyPI issues**: See [PyPI help](https://pypi.org/help/)
- **Trusted Publishers**: Read [PyPI trusted publishing guide](https://docs.pypi.org/trusted-publishers/)
