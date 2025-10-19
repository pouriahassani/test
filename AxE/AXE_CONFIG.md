# AxE Project Configuration & Roadmap

## 🔧 CURRENT PHASE: Temporary Fixes

### Phase 1: Short-Term Temporary Fixes (CURRENT)
**Goal**: Get AxE working reliably without major architectural changes

#### Immediate Fix Categories:
- [ ] **Build System Issues**
  - Fix compilation errors
  - Resolve dependency problems  
  - Ensure consistent builds across environments

- [ ] **Runtime Stability**
  - Fix segmentation faults
  - Handle memory leaks
  - Resolve file I/O issues

- [ ] **Configuration Problems**
  - Fix broken config files
  - Resolve path issues
  - Handle missing dependencies

- [ ] **Basic Functionality**
  - Ensure partitioning algorithms run
  - Fix data output generation
  - Resolve simulation crashes

#### Temporary Fix Strategy:
- **Minimal Changes**: Only what's needed to make it work
- **Quick Solutions**: Band-aid fixes acceptable for now
- **Document Issues**: Note what needs proper fix in Phase 2
- **Preserve Functionality**: Don't break existing research capability

---

## 🚀 FUTURE PHASE: Full Modernization

### Phase 2: Complete Modernization (PLANNED)
**Goal**: Transform into world-class, modular, professional platform

#### Modernization Categories:
- [ ] **Architecture Redesign**
  - Modular component separation
  - Clean API interfaces
  - Professional code structure

- [ ] **Code Quality**
  - Industry-standard practices
  - Comprehensive testing
  - Professional documentation

- [ ] **User Experience**
  - Intuitive configuration
  - Clear error messages
  - Comprehensive tutorials

- [ ] **Research Enhancement**
  - Reproducible experiments
  - Advanced analysis tools
  - Extended benchmark suite

---

## 📋 Issue Tracking

### Current Known Issues (To Fix in Phase 1):

#### **Completed ✅**
1. **VSCode Launch Paths**: Hardcoded `/home/axe/workspace/` paths → Fixed with `${workspaceFolder}` variables
2. **Path Management Documentation**: Created comprehensive guide in `docs/Path-Management-Guide.md`
3. **Python Path Resolution**: Created `axe_paths.py` centralized path management module
4. **Core Python Files Updated**: `defines.py`, `simulator.py`, `run_mpsoc.py` now use modern path management
5. **Implementation Progress Documentation**: Created `docs/IMPLEMENTATION_PROGRESS.md` for detailed change tracking

#### **In Progress 🚧**
6. **Build System Paths**: Makefiles contain hardcoded toolchain paths (partially identified)
7. **RTL Hardware Paths**: Verilog files have hardcoded memory paths

#### **Identified 📋**
8. **Runtime Stability Issues**: Segmentation faults and memory leaks (not yet investigated)
9. **Build System Dependencies**: Missing dependency validation
10. **Additional Python Scripts**: Other `.py` files may need path updates

### Future Improvements (For Phase 2):
*[Will be populated during temporary fix phase]*

---

## 🔄 Progress Tracking

### Phase 1 Status: **MAJOR PROGRESS**
- Temporary fixes identified: **7**
- Temporary fixes completed: **5**
- Critical issues resolved: **2** (VSCode + Python path management)

### Phase 2 Status: **NOT STARTED**
- Modernization planning: **PENDING**

---

## 📝 Notes
- This config file will be updated as we progress
- Document all temporary fixes for proper implementation in Phase 2
- Maintain research functionality throughout all changes
- Focus on stability and reliability in Phase 1

*Last Updated: [Current Session]*