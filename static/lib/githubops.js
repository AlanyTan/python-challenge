// git branch info

async function fetchRepoContents({owner='python-book', repo='python-book', path='', branch='main'}) {
    const url = `https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}`;
    let data;
    try {
      const response = await fetch(url, {
        headers: {
          'Accept': 'application/vnd.github.v3+json',
        },
      });
  
      if (!response.ok) {
        throw new Error(`GitHub API returned status ${response.status}`);
      }
  
      data = await response.json();
  
      // Check if the response is an array (directory contents)
      if (Array.isArray(data)) {
        // data.forEach(item => {
        //   console.log(`list github ${item.type} ${item.name}`);
        // });
      } else {
        console.log('Specified path is not a directory or does not exist.');
      }
    } catch (error) {
      console.error('Error fetching repository contents:', error);
    }
    return data;
  }
async function showRepoContents(path = '', stdLibList = []) {
    try {
      const contents = await fetchRepoContents({path});
      const fileList = document.getElementById('gitRepofileList');
      fileList.innerHTML = ''; // Clear existing list
        if (path !== "") {
            let parent_path = path.split('/');
            const listItem = document.createElement('li');
            const link = document.createElement('a');
            parent_path.pop();
            parent_path=parent_path.join('/');
            link.textContent = "..";
            link.href = `#`;
            link.onclick = (event) => {
            event.preventDefault();
            showRepoContents(parent_path);
            };
            listItem.appendChild(link);
            fileList.appendChild(listItem);
        }

      contents.forEach(item => {
        if (item.name.startsWith('.'))
        {
        } else {
            const listItem = document.createElement('li');
            const link = document.createElement('a');
            link.textContent = item.name + (item.type == "dir" ? "/" : "");
            link.href = '#';
            link.onclick = async (event) => {
              event.preventDefault();
              if (item.type === 'dir') {
                  showRepoContents(item.path);
              } else if (item.type === 'file') {
                  closePopup();
                  console.log(`File selected: ${item.path}`);
                  await fetchGitRepoFile(item.path, stdLibList, window.editor);
              }
            };
            listItem.appendChild(link);
            fileList.appendChild(listItem);
        }
      });
    document.getElementById('virtual-file-name').hidden = true;
    document.getElementById('file-list-popup-ok').hidden = true;;
    showPopup();
    } catch (error) {
      console.error('Error fetching repository contents:', error);
    }
  }

  async function fetchGitRepoFile(path, stdLibList = [],editor = null) {
    //actual_path = "/python-book/" + path;
    const actual_path = "https://raw.githubusercontent.com/python-book/python-book/main/" + path;
    response = await fetch(actual_path);
    if (!response.ok) {
        throw new Error(`${response.status} - Error fetching content of ${path}`);
        }
        //return response.text();
    try {
      data = await response.text();
        if (editor){
          editor.setValue(data);
          const tabId = editor.getWrapperElement().parentElement.dataset.tabId;
          targetTab = document.querySelector(`.tab[data-tab-id="${tabId}"]`)
          targetButton = targetTab.querySelector(`.tab-button`);
          targetButton.textContent = path;
        }
          // Write the file content to the /workdir
      await saveFile(`/workdir/${path}`, data);
      stdout_func(`File ${path} loaded successfully.`);
      // Parse for import statements
      const importRegex = /^(?:from\s+([\w.]+)\s+import\s+([\w*, ]+))|(?:import\s+([\w.]+)(?:\s+as\s+\w+)?)$/gm;
      let match;
      let matches = [];
      while ((match = importRegex.exec(data)) !== null) {
        matches.push(match); 
      }    
      for (match of matches) {
        let packageName, modules;
        if (match[1]) { // from ... import ...
          packageName = match[1];
          modules = match[2].split(',').map(s => s.trim()).filter(s => s); 
        } else { // import ...
          packageName = match[3];
          modules = []; // Fetch the whole package
        }

        // Construct the relative path to the module/package
        if (stdLibList.includes(packageName.split('.')[0])) {
          // skip standard lib imports 
          continue;
        }
        const pathParts = path.split('/');
        pathParts.pop(); // Remove the filename
        // fetch all __init__.py of each level of the package path
        const packagePath = pathParts.concat(packageName.startsWith('..') ? '..' : '', packageName.split('.')).filter(Boolean).join('/');
        let i = -1;
        while ((i = (packagePath + '//').indexOf('/', i + 1)) !== -1) {
          // full module name could be a pkg/mod.py file
          let moduleSuffix = '';
          if ( i > packagePath.length) {
            moduleSuffix = '.py';
          } else {
            moduleSuffix = '/__init__.py'
          }
          try {
            let packageInfo = await fileInfo(`${packagePath.slice(0, i)}${moduleSuffix}`);
            if (packageInfo.exists) {
              continue;
            }
          } catch (error) {
            console.warn(`Did not find local file ${packagePath.slice(0, i)}${moduleSuffix}. trying to download it from github`)
          }
          try {
            await fetchGitRepoFile(packagePath.slice(0, i) + moduleSuffix, stdLibList);
          } catch (error) {
            console.warn(`Error fetching ${packagePath.slice(0, i)}${moduleSuffix}. maybe the package is not correctly defined?`)
          }
        }


        // Fetch the module/package recursively
        for (const module of modules) {
          moduleName = module.split(' as ')[0];
          try {
            await fetchGitRepoFile(`${packagePath}/${moduleName}.py`, stdLibList);
          } catch (error) {
            console.warn(`Error fetching ${packagePath}/${moduleName}.py. maybe ${module} is an object?`);
            if (error.message.startsWith('404')) {
              //likely packageName is a module
              await fetchGitRepoFile(`${packagePath}.py`, stdLibList);
              break;
            }
          }
        }
      }
    } catch (error) {
      console.error(`Error fetching content of ${path}:`, error);
    };
    return 0;
  }


