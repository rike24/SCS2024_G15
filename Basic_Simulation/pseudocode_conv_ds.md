伪代码 Disease_Spread(forest_state, age_list, infection_time, p_spread):
    # 定义函数目标
    # forest_state: 表示森林状态的 N x N 矩阵
    # age_list: 表示树木年龄的 N x N 矩阵
    # infection_time: 记录感染时间的 N x N 矩阵
    # p_spread: 传播的基础概率

    定义 5x5 卷积核 kernel
    kernel = [
        [0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 1.0, 1.0, 1.0, 0.5],
        [0.5, 1.0, 0, 1.0, 0.5],
        [0.5, 1.0, 1.0, 1.0, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5]
    ]

    定义函数 apply_periodic_boundary(matrix):
        # 实现周期性边界条件
        对 matrix 添加宽度为2的边界，并用环绕模式填充

    定义函数 infection_time_factor(duration):
        # 根据感染时间计算传播因子
        返回 min(1, duration / 10)

    定义函数 age_factor(age):
        # 根据树龄计算传播因子
        返回 min(1, age / 100)

    # 应用周期性边界条件
    padded_forest = apply_periodic_boundary(forest_state)
    padded_infection_time = apply_periodic_boundary(infection_time)
    padded_age_list = apply_periodic_boundary(age_list)

    # 创建感染树的掩码 infected_mask
    infected_mask = (padded_forest == 1)

    # 将 infected_mask 矩阵展开为 (25 * N^2) 的二维矩阵
    unfolded_infected = 将 infected_mask 使用卷积核展开

    # 计算邻居传播概率矩阵 P_matrix
    duration_matrix = 将 infection_time 使用 infection_time_factor 映射后展开为与 unfolded_infected 相同的形状
    age_matrix = 将 age_list 使用 age_factor 映射后展开为与 unfolded_infected 相同的形状

    # 将卷积核变为 (25 * 1) 的列向量
    unfolded_kernel = 将 kernel 展开为 (25 * 1)

    # 计算最终的 P_matrix
    P_matrix = unfolded_infected * p_spread * duration_matrix * age_matrix
    P_matrix = P_matrix * unfolded_kernel （按列广播乘法）

    # 计算每个树被感染的概率
    one_minus_P_matrix = 1 - P_matrix
    column_product = 对每列的值进行连乘 (得到 (1 * N^2) 的数组)
    infection_probabilities = 1 - column_product

    # 将感染概率数组转换回 (N * N) 的矩阵
    P_center_infected = 将 infection_probabilities 重塑为 (N, N)

    # 生成随机矩阵 random_matrix
    random_matrix = 随机生成一个大小为 (N, N) 的矩阵，范围为 [0, 1]

    # 更新感染状态
    new_infections = (random_matrix < P_center_infected) 且 (forest_state == -1)
    将 new_infections 对应的 forest_state 单元格更新为感染状态 (1)

    返回更新后的 forest_state


Pseudo-code Disease_Spread(forest_state, age_list, infection_time, p_spread):
    # Define function goal
    # forest_state: Represents the forest state as an N x N matrix
    # age_list: Represents the age of each tree as an N x N matrix
    # infection_time: Records the infection time as an N x N matrix
    # p_spread: Base probability of disease transmission

    Define 5x5 convolution kernel kernel
    kernel = [
        [0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 1.0, 1.0, 1.0, 0.5],
        [0.5, 1.0, 0, 1.0, 0.5],
        [0.5, 1.0, 1.0, 1.0, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5]
    ]

    Define function apply_periodic_boundary(matrix):
        # Implement periodic boundary conditions
        Add a width-2 boundary to matrix and fill using wrap mode

    Define function infection_time_factor(duration):
        # Calculate infection factor based on infection duration
        Return min(1, duration / 10)

    Define function age_factor(age):
        # Calculate infection factor based on tree age
        Return min(1, age / 100)

    # Apply periodic boundary conditions
    padded_forest = apply_periodic_boundary(forest_state)
    padded_infection_time = apply_periodic_boundary(infection_time)
    padded_age_list = apply_periodic_boundary(age_list)

    # Create mask for infected trees infected_mask
    infected_mask = (padded_forest == 1)

    # Unfold infected_mask matrix into a (25 * N^2) 2D matrix
    unfolded_infected = Unfold infected_mask using the convolution kernel

    # Calculate neighbor infection probability matrix P_matrix
    duration_matrix = Map infection_time using infection_time_factor and unfold to match the shape of unfolded_infected
    age_matrix = Map age_list using age_factor and unfold to match the shape of unfolded_infected

    # Transform kernel into a (25 * 1) column vector
    unfolded_kernel = Flatten kernel into a (25 * 1) column vector

    # Compute final P_matrix
    P_matrix = unfolded_infected * p_spread * duration_matrix * age_matrix
    P_matrix = P_matrix * unfolded_kernel (broadcast multiplication across columns)

    # Calculate the probability of each tree being infected
    one_minus_P_matrix = 1 - P_matrix
    column_product = Perform product of all values in each column (resulting in a (1 * N^2) array)
    infection_probabilities = 1 - column_product

    # Reshape infection probability array back into an (N * N) matrix
    P_center_infected = Reshape infection_probabilities into (N, N)

    # Generate random matrix random_matrix
    random_matrix = Generate a random matrix of size (N, N) with values in [0, 1]

    # Update infection status
    new_infections = (random_matrix < P_center_infected) AND (forest_state == -1)
    Update corresponding cells in forest_state for new_infections to infected state (1)

    Return the updated forest_state

