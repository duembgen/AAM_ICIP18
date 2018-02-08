clc; clearvars; close all;

%% Read the mat files
distances_4 = load('distances_4.mat');
distances_4 = distances_4.distancesCol;

distances_6 = load('distances_6.mat');
distances_6 = distances_6.distancesCol;

distances_7 = load('distances_7.mat');
distances_7 = distances_7.distancesCol;


GaussStd2Color_4 = load('GaussStd2Color_4.mat');
GaussStd2Color_4 = GaussStd2Color_4.GaussStd2Color;

GaussStd2Color_6 = load('GaussStd2Color_6.mat');
GaussStd2Color_6 = GaussStd2Color_6.GaussStd2Color;

GaussStd2Color_7 = load('GaussStd2Color_7.mat');
GaussStd2Color_7 = GaussStd2Color_7.GaussStd2Color;

GaussStd2Nir_4 = load('GaussStd2Nir_4.mat');
GaussStd2Nir_4 = GaussStd2Nir_4.GaussStd2Nir;

GaussStd2Nir_6 = load('GaussStd2Nir_6.mat');
GaussStd2Nir_6 = GaussStd2Nir_6.GaussStd2Nir;

GaussStd2Nir_7 = load('GaussStd2Nir_7.mat');
GaussStd2Nir_7 = GaussStd2Nir_7.GaussStd2Nir;

%Compute deltas
delta1_4 = GaussStd2Color_4(:,1) - GaussStd2Color_4(:,2);
delta2_4 = GaussStd2Nir_4.' - GaussStd2Color_4(:,2);

delta1_6 = GaussStd2Color_6(:,1) - GaussStd2Color_6(:,2);
delta2_6 = GaussStd2Nir_6.' - GaussStd2Color_6(:,2);

delta1_7 = GaussStd2Color_7(:,1) - GaussStd2Color_7(:,2);
delta2_7 = GaussStd2Nir_7.' - GaussStd2Color_7(:,2);


%% Figures
Lwidth = 3;
%%%%%%%%%%%%%%%%%%%
figure;
plot(distances_4, GaussStd2Color_4(:,1), 'r', 'LineWidth',Lwidth); hold on;
plot(distances_4, GaussStd2Color_4(:,2), 'g', 'LineWidth',Lwidth); hold on;
plot(distances_4, GaussStd2Color_4(:,3), 'b', 'LineWidth',Lwidth); hold on;
plot(distances_4, GaussStd2Nir_4, 'k', 'LineWidth',Lwidth); 

xlim([distances_4(1), distances_4(end)]);
ylim([0 70]); set(gca,'FontSize',16);

xlabel('Distance (mm)', 'FontSize', 20);
ylabel('PSF standard deviation (pixels)', 'FontSize', 20);


figure;
plot(distances_4, delta1_4, 'r', 'LineWidth',Lwidth); hold on;
plot(distances_4, delta2_4, 'k', 'LineWidth',Lwidth); 
plot([distances_4(1) distances_4(end)],[0 0],'--k');

xlim([distances_4(1), distances_4(end)]);
ylim([-20 20]); set(gca,'FontSize',16);

xlabel('Distance (mm)', 'FontSize', 20);
ylabel('\Delta', 'FontSize', 20);
%%%%%%%%%%%%%%%%%%%
figure;
plot(distances_6, GaussStd2Color_6(:,1), 'r', 'LineWidth',Lwidth); hold on;
plot(distances_6, GaussStd2Color_6(:,2), 'g', 'LineWidth',Lwidth); hold on;
plot(distances_6, GaussStd2Color_6(:,3), 'b', 'LineWidth',Lwidth); hold on;
plot(distances_6, GaussStd2Nir_6, 'k', 'LineWidth',Lwidth);

xlim([distances_6(1), distances_6(end)]);
ylim([0 70]); set(gca,'FontSize',16);

xlabel('Distance (mm)', 'FontSize', 20);
ylabel('PSF standard deviation (pixels)', 'FontSize', 20);


figure;
plot(distances_6, delta1_6, 'r', 'LineWidth',Lwidth); hold on;
plot(distances_6, delta2_6, 'k', 'LineWidth',Lwidth);
plot([distances_6(1) distances_6(end)],[0 0],'--k');

xlim([distances_6(1), distances_6(end)]);
ylim([-20 20]); set(gca,'FontSize',16);

xlabel('Distance (mm)', 'FontSize', 20);
ylabel('\Delta', 'FontSize', 20);
%%%%%%%%%%%%%%%%%%%
figure;
plot(distances_7, GaussStd2Color_7(:,1), 'r', 'LineWidth',Lwidth); hold on;
plot(distances_7, GaussStd2Color_7(:,2), 'g', 'LineWidth',Lwidth); hold on;
plot(distances_7, GaussStd2Color_7(:,3), 'b', 'LineWidth',Lwidth); hold on;
plot(distances_7, GaussStd2Nir_7, 'k', 'LineWidth',Lwidth);

xlim([distances_7(1), distances_7(end)]);
ylim([0 70]); set(gca,'FontSize',16);

xlabel('Distance (mm)', 'FontSize', 20);
ylabel('PSF standard deviation (pixels)', 'FontSize', 20);


figure;
plot(distances_7, delta1_7, 'r', 'LineWidth',Lwidth); hold on;
plot(distances_7, delta2_7, 'k', 'LineWidth',Lwidth);
plot([distances_7(1) distances_7(end)],[0 0],'--k');

xlim([distances_7(1), distances_7(end)]);
ylim([-20 20]); set(gca,'FontSize',16);

xlabel('Distance (mm)', 'FontSize', 20);
ylabel('\Delta', 'FontSize', 20);



