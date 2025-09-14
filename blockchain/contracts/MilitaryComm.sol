// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title MilitaryComm
 * @dev Secure Military Communication System Smart Contract
 * @notice Handles command center authority, device authentication, and secure message logging
 */
contract MilitaryComm {
    // ===== STATE VARIABLES =====
    
    address public commandCenter;
    uint256 public globalLamportClock;
    
    enum OperationalMode { NORMAL, EMERGENCY, RESYNC, MAINTENANCE }
    OperationalMode public currentMode;
    
    enum DeviceType { MOBILE, BASE, COMMAND }
    enum AuthLevel { UNVERIFIED, BASIC, STANDARD, CLASSIFIED, TOP_SECRET }
    
    struct Device {
        address deviceAddress;
        string deviceId;
        DeviceType deviceType;
        AuthLevel authLevel;
        bool isActive;
        bool isAuthenticated;
        uint256 lastSeen;
        string publicKey;
        uint256 messageCount;
    }
    
    struct Message {
        string messageId;
        string fromDeviceId;
        string toDeviceId;
        string encryptedPayload;
        bytes32 payloadHash;
        uint256 timestamp;
        uint256 lamportClock;
        bool isAnomaly;
        OperationalMode modeWhenSent;
    }
    
    struct BlockchainLog {
        bytes32 txHash;
        string fromDevice;
        string toDevice;
        bytes32 messageHash;
        uint256 timestamp;
        uint256 lamportClock;
        OperationalMode mode;
        bool isResync;
    }
    
    // ===== MAPPINGS =====
    
    mapping(string => Device) public devices;
    mapping(string => Message) public messages;
    mapping(bytes32 => BlockchainLog) public blockchainLogs;
    mapping(address => bool) public authorizedOperators;
    mapping(string => bool) public deviceExists;
    
    // ===== ARRAYS =====
    
    string[] public deviceList;
    string[] public messageList;
    bytes32[] public logList;
    
    // ===== EVENTS =====
    
    event CommandCenterChanged(address indexed oldCenter, address indexed newCenter);
    event ModeChanged(OperationalMode indexed oldMode, OperationalMode indexed newMode, address indexed changedBy);
    event DeviceRegistered(string indexed deviceId, DeviceType deviceType, AuthLevel authLevel);
    event DeviceAuthenticated(string indexed deviceId, address indexed deviceAddress);
    event DeviceDeactivated(string indexed deviceId, string reason);
    event MessageLogged(string indexed messageId, string indexed fromDevice, string indexed toDevice, bool isAnomaly);
    event EmergencyModeActivated(address indexed activatedBy, string reason);
    event BlockchainLogCreated(bytes32 indexed txHash, string fromDevice, string toDevice);
    event AnomalyDetected(string indexed messageId, string indexed deviceId, string alertType);
    
    // ===== MODIFIERS =====
    
    modifier onlyCommandCenter() {
        require(msg.sender == commandCenter, "Only command center can perform this action");
        _;
    }
    
    modifier onlyAuthorized() {
        require(
            msg.sender == commandCenter || authorizedOperators[msg.sender],
            "Not authorized to perform this action"
        );
        _;
    }
    
    modifier deviceMustExist(string memory deviceId) {
        require(deviceExists[deviceId], "Device does not exist");
        _;
    }
    
    modifier onlyActiveDevice(string memory deviceId) {
        require(devices[deviceId].isActive, "Device is not active");
        _;
    }
    
    modifier onlyAuthenticatedDevice(string memory deviceId) {
        require(devices[deviceId].isAuthenticated, "Device is not authenticated");
        _;
    }
    
    // ===== CONSTRUCTOR =====
    
    constructor() {
        commandCenter = msg.sender;
        currentMode = OperationalMode.NORMAL;
        globalLamportClock = 0;
        authorizedOperators[msg.sender] = true;
        
        emit CommandCenterChanged(address(0), commandCenter);
        emit ModeChanged(OperationalMode.NORMAL, OperationalMode.NORMAL, msg.sender);
    }
    
    // ===== COMMAND CENTER FUNCTIONS =====
    
    /**
     * @dev Transfer command center authority
     */
    function transferCommandCenter(address newCommandCenter) external onlyCommandCenter {
        require(newCommandCenter != address(0), "Invalid address");
        address oldCenter = commandCenter;
        commandCenter = newCommandCenter;
        authorizedOperators[newCommandCenter] = true;
        
        emit CommandCenterChanged(oldCenter, newCommandCenter);
    }
    
    /**
     * @dev Change operational mode
     */
    function changeOperationalMode(OperationalMode newMode, string memory reason) external onlyAuthorized {
        OperationalMode oldMode = currentMode;
        currentMode = newMode;
        globalLamportClock++;
        
        emit ModeChanged(oldMode, newMode, msg.sender);
        
        if (newMode == OperationalMode.EMERGENCY) {
            emit EmergencyModeActivated(msg.sender, reason);
        }
    }
    
    /**
     * @dev Add authorized operator
     */
    function addAuthorizedOperator(address operator) external onlyCommandCenter {
        authorizedOperators[operator] = true;
    }
    
    /**
     * @dev Remove authorized operator
     */
    function removeAuthorizedOperator(address operator) external onlyCommandCenter {
        require(operator != commandCenter, "Cannot remove command center");
        authorizedOperators[operator] = false;
    }
    
    // ===== DEVICE MANAGEMENT FUNCTIONS =====
    
    /**
     * @dev Register a new device
     */
    function registerDevice(
        string memory deviceId,
        DeviceType deviceType,
        AuthLevel authLevel,
        string memory publicKey
    ) external onlyAuthorized {
        require(!deviceExists[deviceId], "Device already exists");
        require(bytes(deviceId).length > 0, "Device ID cannot be empty");
        require(bytes(publicKey).length > 0, "Public key cannot be empty");
        
        devices[deviceId] = Device({
            deviceAddress: address(0),
            deviceId: deviceId,
            deviceType: deviceType,
            authLevel: authLevel,
            isActive: true,
            isAuthenticated: false,
            lastSeen: block.timestamp,
            publicKey: publicKey,
            messageCount: 0
        });
        
        deviceExists[deviceId] = true;
        deviceList.push(deviceId);
        globalLamportClock++;
        
        emit DeviceRegistered(deviceId, deviceType, authLevel);
    }
    
    /**
     * @dev Authenticate a device
     */
    function authenticateDevice(string memory deviceId, address deviceAddress) 
        external 
        onlyAuthorized 
        deviceMustExist(deviceId) 
    {
        require(deviceAddress != address(0), "Invalid device address");
        
        devices[deviceId].deviceAddress = deviceAddress;
        devices[deviceId].isAuthenticated = true;
        devices[deviceId].lastSeen = block.timestamp;
        globalLamportClock++;
        
        emit DeviceAuthenticated(deviceId, deviceAddress);
    }
    
    /**
     * @dev Deactivate a device
     */
    function deactivateDevice(string memory deviceId, string memory reason) 
        external 
        onlyAuthorized 
        deviceMustExist(deviceId) 
    {
        devices[deviceId].isActive = false;
        devices[deviceId].isAuthenticated = false;
        globalLamportClock++;
        
        emit DeviceDeactivated(deviceId, reason);
    }
    
    /**
     * @dev Update device last seen timestamp
     */
    function updateDeviceLastSeen(string memory deviceId) 
        external 
        deviceMustExist(deviceId) 
        onlyActiveDevice(deviceId) 
    {
        devices[deviceId].lastSeen = block.timestamp;
    }
    
    // ===== MESSAGE LOGGING FUNCTIONS =====
    
    /**
     * @dev Log a secure message to blockchain
     */
    function logMessage(
        string memory messageId,
        string memory fromDeviceId,
        string memory toDeviceId,
        string memory encryptedPayload,
        bytes32 payloadHash,
        bool isAnomaly
    ) external onlyAuthorized 
        deviceMustExist(fromDeviceId) 
        deviceMustExist(toDeviceId)
        onlyAuthenticatedDevice(fromDeviceId) 
    {
        require(bytes(messageId).length > 0, "Message ID cannot be empty");
        require(payloadHash != bytes32(0), "Payload hash cannot be empty");
        
        messages[messageId] = Message({
            messageId: messageId,
            fromDeviceId: fromDeviceId,
            toDeviceId: toDeviceId,
            encryptedPayload: encryptedPayload,
            payloadHash: payloadHash,
            timestamp: block.timestamp,
            lamportClock: globalLamportClock,
            isAnomaly: isAnomaly,
            modeWhenSent: currentMode
        });
        
        messageList.push(messageId);
        devices[fromDeviceId].messageCount++;
        devices[fromDeviceId].lastSeen = block.timestamp;
        globalLamportClock++;
        
        emit MessageLogged(messageId, fromDeviceId, toDeviceId, isAnomaly);
        
        if (isAnomaly) {
            emit AnomalyDetected(messageId, fromDeviceId, "Message content anomaly");
        }
        
        // Create blockchain log
        bytes32 logHash = keccak256(abi.encodePacked(messageId, fromDeviceId, toDeviceId, block.timestamp));
        _createBlockchainLog(logHash, fromDeviceId, toDeviceId, payloadHash);
    }
    
    /**
     * @dev Internal function to create blockchain log
     */
    function _createBlockchainLog(
        bytes32 txHash,
        string memory fromDevice,
        string memory toDevice,
        bytes32 messageHash
    ) internal {
        blockchainLogs[txHash] = BlockchainLog({
            txHash: txHash,
            fromDevice: fromDevice,
            toDevice: toDevice,
            messageHash: messageHash,
            timestamp: block.timestamp,
            lamportClock: globalLamportClock,
            mode: currentMode,
            isResync: currentMode == OperationalMode.RESYNC
        });
        
        logList.push(txHash);
        
        emit BlockchainLogCreated(txHash, fromDevice, toDevice);
    }
    
    // ===== EMERGENCY FUNCTIONS =====
    
    /**
     * @dev Emergency shutdown - deactivate all devices
     */
    function emergencyShutdown(string memory reason) external onlyCommandCenter {
        currentMode = OperationalMode.EMERGENCY;
        
        for (uint i = 0; i < deviceList.length; i++) {
            devices[deviceList[i]].isActive = false;
            devices[deviceList[i]].isAuthenticated = false;
        }
        
        globalLamportClock++;
        
        emit EmergencyModeActivated(msg.sender, reason);
        emit ModeChanged(OperationalMode.NORMAL, OperationalMode.EMERGENCY, msg.sender);
    }
    
    /**
     * @dev Bulk authenticate devices after emergency
     */
    function bulkAuthenticateDevices(string[] memory deviceIds) external onlyCommandCenter {
        require(currentMode == OperationalMode.EMERGENCY, "Only available in emergency mode");
        
        for (uint i = 0; i < deviceIds.length; i++) {
            if (deviceExists[deviceIds[i]]) {
                devices[deviceIds[i]].isActive = true;
                devices[deviceIds[i]].isAuthenticated = true;
                devices[deviceIds[i]].lastSeen = block.timestamp;
            }
        }
        
        globalLamportClock++;
    }
    
    // ===== VIEW FUNCTIONS =====
    
    /**
     * @dev Get device information
     */
    function getDevice(string memory deviceId) external view returns (Device memory) {
        require(deviceExists[deviceId], "Device does not exist");
        return devices[deviceId];
    }
    
    /**
     * @dev Get message information
     */
    function getMessage(string memory messageId) external view returns (Message memory) {
        return messages[messageId];
    }
    
    /**
     * @dev Get blockchain log information
     */
    function getBlockchainLog(bytes32 txHash) external view returns (BlockchainLog memory) {
        return blockchainLogs[txHash];
    }
    
    /**
     * @dev Get total device count
     */
    function getDeviceCount() external view returns (uint256) {
        return deviceList.length;
    }
    
    /**
     * @dev Get total message count
     */
    function getMessageCount() external view returns (uint256) {
        return messageList.length;
    }
    
    /**
     * @dev Get total blockchain log count
     */
    function getLogCount() external view returns (uint256) {
        return logList.length;
    }
    
    /**
     * @dev Get active device count
     */
    function getActiveDeviceCount() external view returns (uint256) {
        uint256 activeCount = 0;
        for (uint i = 0; i < deviceList.length; i++) {
            if (devices[deviceList[i]].isActive) {
                activeCount++;
            }
        }
        return activeCount;
    }
    
    /**
     * @dev Get authenticated device count
     */
    function getAuthenticatedDeviceCount() external view returns (uint256) {
        uint256 authCount = 0;
        for (uint i = 0; i < deviceList.length; i++) {
            if (devices[deviceList[i]].isAuthenticated) {
                authCount++;
            }
        }
        return authCount;
    }
    
    /**
     * @dev Check if address is authorized
     */
    function isAuthorized(address account) external view returns (bool) {
        return authorizedOperators[account] || account == commandCenter;
    }
    
    /**
     * @dev Get system status
     */
    function getSystemStatus() external view returns (
        address _commandCenter,
        OperationalMode _currentMode,
        uint256 _globalLamportClock,
        uint256 _totalDevices,
        uint256 _activeDevices,
        uint256 _totalMessages
    ) {
        return (
            commandCenter,
            currentMode,
            globalLamportClock,
            deviceList.length,
            this.getActiveDeviceCount(),
            messageList.length
        );
    }
}