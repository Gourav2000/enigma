const { app, BrowserWindow } = require('electron')
const child_process = require('child_process')

function createWindow() {
    var workerProcess = child_process.spawn('Makewin');
    var session_data;
    workerProcess.stdout.on('data', function(data) {

        console.log('stdout: ' + data);
        session_data = JSON.parse(data.toString())
        console.log(session_data)
        const win = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                nodeIntegration: true,
                enableRemoteModule: true
            }
        })

        win.setMenuBarVisibility(false)

        win.loadFile('index.html')

        win.webContents.on('did-finish-load', function() {
            win.webContents.send('session_data', session_data);
        });

    });

    workerProcess.stderr.on('data', function(data) {
        process.exit(0);
        console.log('stderr: ' + data);
    });
    workerProcess.on('close', function(code) {
        console.log('child process exited with code ' + code);
        isWindowOpen = false;
        process.exit(0);

    });

}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})