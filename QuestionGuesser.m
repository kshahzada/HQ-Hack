API_KEY = 'AIzaSyAy-Twv2K3ukFiMfRHMWhjG9ZSP0h9RJ_A';

vid = videoinput('winvideo', 1, 'MJPG_1280x720');
src = getselectedsource(vid);
set(vid, 'ReturnedColorSpace', 'RGB');


vid.FramesPerTrigger = 1;

preview(vid);

while true
    % wait for user input
    input('Ready?');
    
    % take photo
    img = getsnapshot(vid);
    
    %read text
    visionAPI = strcat('https://vision.googleapis.com/v1/images:annotate?key=', API_KEY);

    data = '';%struct('api_key',writeApiKey,'field1',data);
    options = weboptions('MediaType','application/json');
   %response = webwrite(visionAPI,data,options)
    
    %print answer
    fprintf('\n******************\nNew answer:\n')
    fprintf('<strong>A</strong>\n')
end