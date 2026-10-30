"""EV3 Legendary가 연결된 PC의 시리얼 포트를 확인하는 진단 도구.

이 코드는 포트 목록만 출력합니다. 장치를 열거나 데이터를 보내지 않습니다.
Thonny의 Python에 pyserial 설치 필요: 도구 → 패키지 관리 → pyserial
"""
try:
    from serial.tools import list_ports
except ImportError:
    print("pyserial이 없습니다. Thonny → 도구 → 패키지 관리에서 pyserial을 설치하세요.")
else:
    ports = list(list_ports.comports())
    if not ports:
        print("Python에서 조회되는 시리얼 포트가 없습니다.")
        print("Chrome Web Serial 연결이 성공했어도 Python 접근은 별도 확인이 필요합니다.")
    for port in ports:
        print(f"포트: {port.device}")
        print(f"  설명: {port.description}")
        print(f"  HWID: {port.hwid}")
        print("  ---")

print("이 진단 코드는 EV3에 아무 명령도 보내지 않습니다.")
