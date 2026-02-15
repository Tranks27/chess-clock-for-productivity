# Release Notes - v1.3.0

## Highlights
✨ **Idle Detection** - App now automatically catches AFK time after 5 minutes
📊 **Smarter Stats** - Monthly file organization keeps everything clean
📅 **Calendar View** - Browse and analyze your work history by date
🎯 **Better UX** - Custom time input, improved dialogs, consistent styling

---

## What's New

### 🎯 Idle Detection
- Detects 5 minutes of inactivity, prompts to switch to Slack
- Auto-switches after 3 minutes with confirmation popup

### 📊 Monthly Stats Organization
- Stats split into YYYY-MM.json files for better organization

### 📅 Interactive Calendar
- Browse work history by date with month navigation

### ⏰ Custom Time Input
- Hour and minute fields with +/- buttons

### 🏗️ Code Refactoring
- Modular architecture with separate modules in `/src`

## Fixes
- Audio path resolution for .exe builds
- Calendar navigation stability
- Stats dashboard styling consistency

## New Dependency
- `pynput>=1.8.1` (for mouse tracking)

---

**Version:** 1.3.0
**Status:** Production Ready
