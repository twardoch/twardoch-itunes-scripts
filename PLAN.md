# Improvement Plan for twardoch-itunes-scripts

## Executive Summary

This repository contains two Python scripts from 2006 that interact with iTunes libraries. The scripts are outdated and need comprehensive modernization to work with current systems and follow modern Python best practices. This plan outlines a complete overhaul to transform these scripts into a maintainable, installable Python package.

## Current State Analysis

### Technical Debt
1. **Python Version**: Written for Python 2.x, needs Python 3 compatibility
2. **Dependencies**: Uses deprecated/unmaintained libraries (win32com, appscript, old mutagen API)
3. **API Integration**: Audioscrobbler API is deprecated (now Last.fm with different endpoints)
4. **Platform Support**: Windows-centric with incomplete Mac support, no Linux support
5. **Code Quality**: No type hints, inconsistent naming, minimal error handling
6. **Project Structure**: Flat structure with no modularity
7. **Distribution**: No packaging, dependency management, or installation process

### Functional Issues
1. iTunes COM interface may not work with modern Music app
2. Audioscrobbler endpoints no longer exist
3. ID3 tag handling may conflict with modern music players
4. No configuration options or CLI interface
5. Hardcoded values throughout the code

## Modernization Strategy

### Phase 1: Foundation and Structure (Week 1)

#### 1.1 Project Restructuring
Create a proper Python package structure:
```
twardoch-itunes-scripts/
├── src/
│   └── itunes_tools/
│       ├── __init__.py
│       ├── __main__.py          # CLI entry point
│       ├── config.py            # Configuration management
│       ├── models.py            # Data models
│       ├── platforms/           # Platform-specific implementations
│       │   ├── __init__.py
│       │   ├── base.py         # Abstract base class
│       │   ├── windows.py      # Windows implementation
│       │   ├── macos.py        # macOS implementation
│       │   └── linux.py        # Linux stub/alternative
│       ├── services/
│       │   ├── __init__.py
│       │   ├── itunes.py       # iTunes/Music app interface
│       │   ├── lastfm.py       # Last.fm API client
│       │   └── id3.py          # ID3 tag handling
│       ├── commands/            # CLI commands
│       │   ├── __init__.py
│       │   ├── autorate.py
│       │   └── sync_ratings.py
│       └── utils/
│           ├── __init__.py
│           ├── logging.py
│           └── progress.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
│   ├── index.md
│   ├── installation.md
│   ├── usage.md
│   └── api.md
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── release.yml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── setup.cfg
├── tox.ini
├── .gitignore
├── .pre-commit-config.yaml
└── Makefile
```

#### 1.2 Development Environment Setup
1. Create `pyproject.toml` with modern Python packaging standards
2. Set up virtual environment management with poetry or pip-tools
3. Configure pre-commit hooks for code quality
4. Set up tox for multi-version testing
5. Configure GitHub Actions for CI/CD

#### 1.3 Code Quality Tools
- **Linting**: ruff, pylint
- **Formatting**: black, isort
- **Type Checking**: mypy with strict mode
- **Security**: bandit, safety
- **Documentation**: Sphinx with autodoc
- **Testing**: pytest with coverage

### Phase 2: Core Refactoring (Week 2-3)

#### 2.1 Platform Abstraction Layer
Create an abstract base class for iTunes/Music app interaction:
```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class MusicLibraryInterface(ABC):
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to music library"""
        
    @abstractmethod
    def get_tracks(self) -> List[Track]:
        """Retrieve all tracks from library"""
        
    @abstractmethod
    def update_rating(self, track_id: str, rating: int) -> bool:
        """Update track rating"""
```

Implement platform-specific versions:
- Windows: Use pywin32 or comtypes for COM automation
- macOS: Investigate Music.app AppleScript or use py-applescript
- Linux: Provide alternative using local file scanning

#### 2.2 Modern API Integration
Replace Audioscrobbler with Last.fm API v2:
1. Implement OAuth2 authentication flow
2. Create async API client using httpx
3. Add rate limiting and retry logic
4. Cache API responses to reduce calls
5. Handle API errors gracefully

#### 2.3 ID3 Tag Handling
Update mutagen integration:
1. Use latest mutagen API
2. Support multiple audio formats (MP3, M4A, FLAC)
3. Preserve existing tags when updating
4. Add validation for tag values
5. Implement batch operations for performance

### Phase 3: Feature Enhancement (Week 4)

#### 3.1 Configuration System
Implement hierarchical configuration:
1. Command-line arguments (highest priority)
2. Environment variables
3. User config file (~/.config/itunes-tools/config.yaml)
4. System defaults

Configuration options:
- Last.fm API credentials
- Rating scale mapping
- File type filters
- Logging levels
- Progress display options

#### 3.2 CLI Interface
Create intuitive CLI using Click or Typer:
```bash
# Auto-rate tracks
itunes-tools autorate --artist "Pink Floyd" --min-popularity 0.7

# Sync ratings bidirectionally
itunes-tools sync-ratings --direction both --format popm

# Export library metadata
itunes-tools export --format json --output library.json

# Show statistics
itunes-tools stats --group-by artist
```

#### 3.3 Advanced Features
1. **Playlist Management**: Create playlists based on ratings
2. **Bulk Operations**: Process specific artists/albums/playlists
3. **Dry Run Mode**: Preview changes before applying
4. **Backup/Restore**: Save and restore rating snapshots
5. **Web Interface**: Optional Flask/FastAPI web UI

### Phase 4: Testing and Documentation (Week 5)

#### 4.1 Testing Strategy
1. **Unit Tests**: 
   - Test each module in isolation
   - Mock external dependencies
   - Aim for >80% coverage

2. **Integration Tests**:
   - Test platform-specific implementations
   - Test Last.fm API integration
   - Test ID3 tag operations

3. **End-to-End Tests**:
   - Test complete workflows
   - Use test fixtures with sample music files
   - Test error scenarios

#### 4.2 Documentation
1. **User Documentation**:
   - Installation guide for each platform
   - Quick start tutorial
   - Command reference
   - Troubleshooting guide

2. **Developer Documentation**:
   - Architecture overview
   - API reference
   - Contributing guidelines
   - Plugin development guide

3. **Examples**:
   - Common use cases
   - Automation scripts
   - Integration examples

### Phase 5: Distribution and Deployment (Week 6)

#### 5.1 Packaging
1. Build wheel and sdist packages
2. Create platform-specific installers:
   - Windows: MSI installer or portable exe
   - macOS: Homebrew formula
   - Linux: Snap/Flatpak/AppImage

#### 5.2 Release Process
1. Semantic versioning (follow SemVer)
2. Automated releases via GitHub Actions
3. Publish to PyPI
4. Generate release notes from commits
5. Create GitHub releases with binaries

#### 5.3 Community Building
1. Create issue templates
2. Set up discussions forum
3. Write contribution guidelines
4. Create code of conduct
5. Set up project website

## Migration Path for Existing Users

### Compatibility Mode
Provide a compatibility layer that:
1. Accepts old command-line arguments
2. Translates old config formats
3. Provides migration warnings
4. Offers automated migration tools

### Data Migration
1. Detect existing POPM tags
2. Offer to backup current ratings
3. Provide rollback mechanism
4. Generate migration report

## Performance Optimizations

1. **Concurrent Processing**: Use asyncio for API calls
2. **Batch Operations**: Process files in chunks
3. **Caching**: Cache API responses and file metadata
4. **Progress Indicators**: Provide real-time feedback
5. **Memory Management**: Stream large libraries

## Security Considerations

1. **API Credentials**: Use secure storage (keyring)
2. **File Permissions**: Respect OS file permissions
3. **Input Validation**: Sanitize all user inputs
4. **Dependency Scanning**: Regular security audits
5. **Privacy**: Don't log sensitive information

## Maintenance Plan

1. **Regular Updates**:
   - Monthly dependency updates
   - Quarterly feature releases
   - Security patches as needed

2. **Monitoring**:
   - Error tracking with Sentry
   - Usage analytics (opt-in)
   - Performance metrics

3. **Community Engagement**:
   - Respond to issues within 48 hours
   - Monthly development updates
   - Quarterly roadmap reviews

## Success Metrics

1. **Code Quality**: 
   - Test coverage > 80%
   - No critical security issues
   - Type coverage > 90%

2. **User Adoption**:
   - 100+ GitHub stars
   - 1000+ PyPI downloads/month
   - Active community contributions

3. **Performance**:
   - Process 10k tracks < 1 minute
   - API response caching > 90% hit rate
   - Memory usage < 100MB for typical library

## Risk Mitigation

1. **Platform Changes**: Abstract platform-specific code
2. **API Deprecation**: Support multiple API versions
3. **Library Updates**: Pin dependencies, test updates
4. **User Data Loss**: Always backup before modifications
5. **Performance Issues**: Profile and optimize bottlenecks

## Conclusion

This comprehensive modernization plan will transform the outdated iTunes scripts into a professional, maintainable Python package. The phased approach ensures steady progress while maintaining stability. The focus on testing, documentation, and community building will ensure long-term sustainability of the project.