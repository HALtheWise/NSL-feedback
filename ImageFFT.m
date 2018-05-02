%ImageFFT

%% Editing Image

% Orig = imread('2018-40-23-13_40.png'); %Finding original imageOrig = imread('2018-40-23-13_40.png'); %Finding original image
% Orig = imread('2018-04-25--12-09-22.png'); %Finding original image
Orig = imread('2018-46-11-11_46.png');


greyIm = rgb2gray(Orig); %Making it grey instead of colored

greyIm = im2double(greyIm); %Convert to double precision so we can actually do stuff


[size1,size2] = size(greyIm); %Finding sizes
minsize = min(size1,size2)/2; %Length of square we're cropping
greyIm = greyIm(floor(size1/2-minsize/2):floor(size1/2 + minsize/2), floor(size2/2 - minsize/2): floor(size2/2 +minsize/2)); %CROP

a = mean(mean(greyIm)); %find mean value
greyIm2 = greyIm - a; %get rid of mean value

fftim = abs(fftshift(fft2(greyIm2))); %find FFT

%% Manipulating the FFT

fftsize = size(fftim); 

fftcenter = ceil(fftsize/2);

deltaR = 3;
maxrad =floor(sqrt(fftsize(1)^2 + fftsize(2)^2)/2);
intensitysum = zeros(ceil(maxrad/deltaR),1);
divisionfac = intensitysum;
angleintensitysum = zeros(360,1);
anglediv = angleintensitysum;
for i = 1:fftsize(1)
    for j = 1:fftsize(2)
        r = sqrt((i-fftcenter(1))^2 + (j-fftcenter(2))^2);
        rindex = floor(r/deltaR) +1;
        if rindex<maxrad
            intensitysum(rindex) = intensitysum(rindex) + fftim(i,j);
            divisionfac(rindex) = divisionfac(rindex) + 1;
        end
        
        
        angle = floor(atan2d((j-fftcenter(2)),(i-fftcenter(1))));
        if angle<0
            angle = 360 + angle;
        end
        
        angle = angle+1;
        if angle == 0
            angle
        end
        angleintensitysum(angle) = angleintensitysum(angle) + fftim(i,j);
        anglediv(angle) = anglediv(angle)+1;
    end
end

radialintensity = intensitysum./divisionfac;
radius = 0:deltaR:deltaR*(length(radialintensity)-1);

angleintensity = angleintensitysum./anglediv;
anglerange = 0:359;
%% Plotting
figure 
subplot(2,2,1)
imshow(greyIm);  %Cropped version of image            
drawnow

subplot(2,2,2)
imagesc(fftim) % FFT
axis square
drawnow

subplot(2,2,3)
loglog(radius,radialintensity)
drawnow

subplot(2,2,4)
plot(anglerange,angleintensity)
drawnow
