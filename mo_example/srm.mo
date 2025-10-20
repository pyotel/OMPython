model SMR_PowerPlant
  // ===== Parameters =====
  parameter Real Q_fission = 1e8 "열출력 [W]";
  parameter Real eff_thermal = 0.35 "열 → 전기 변환 효율";
  parameter Real m_coolant = 500 "냉각재 질량 [kg]";
  parameter Real Cp = 4200 "냉각재 비열 [J/kgK]";
  parameter Real T_in = 300 "냉각재 입구온도 [K]";
  parameter Real T_steam = 550 "증기 온도 [K]";
  parameter Real UA = 5e4 "열교환기 전달계수 [W/K]";
  
  // ===== Variables =====
  Real T_core(start=320) "노심 냉각수 온도 [K]";
  Real Q_transfer "냉각수 → 증기 열전달량 [W]";
  Real P_electric "전력 출력 [W]";
  
  // ===== Equations =====
equation
  // 노심에서 냉각수로 열 전달
  der(T_core) = (Q_fission - Q_transfer) / (m_coolant * Cp);
  
  // 열교환기에서 열 전달 (단순 UA 모델)
  Q_transfer = UA * (T_core - T_steam);
  
  // 열교환된 열 중 일부가 발전으로 변환
  P_electric = Q_transfer * eff_thermal;
  
  // 출력 관계 (예시용)
  // 전력 출력이 시간에 따라 안정화되는 형태를 시뮬레이션 가능
end SMR_PowerPlant;

